# coding=ascii
import json
import numpy as np
import os
from collections import namedtuple

import tensorflow as tf
from tensorflow import Session, Graph

from maya import OpenMaya, OpenMayaMPx

from fdda import utils as maya_utils
from fdda.logger import log


TFModel = namedtuple("TFModel", ["graph", "session", "input_tensor", "output_tensor", "vertices"])


class FDDADeformerNode(OpenMayaMPx.MPxDeformerNode):
    kNodeName = "fdda"
    kNodeID = OpenMaya.MTypeId(0x0012d5c1)

    kModels = "models"
    kJointMap = "joint_map"
    kMeta = "meta"
    kRoot = "root"
    kInput = "input"
    kOutput = "output"

    # Attributes
    DATA_LOCATION = OpenMaya.MObject()
    IN_MATRICES = OpenMaya.MObject()

    kTrainingDataLong = "trainingData"
    kTrainingDataShort = "ta"
    kMatrixLong = "matrix"
    kMatrixShort = "mat"

    def __init__(self, *args, **kwargs):
        super(FDDADeformerNode, self).__init__(*args, **kwargs)

        self.data_location = None
        self.location_changed = True
        self.models = list()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(DataLocation: {self.data_location})"

    def _clear(self):
        self.data_location = None
        self.models = list()

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(cls())

    @classmethod
    def initialize(cls):
        in_attrs = list()
        out_attrs = list()

        # Inputs
        td_attr = OpenMaya.MFnTypedAttribute()
        cls.DATA_LOCATION = td_attr.create("trainingData", "ta", OpenMaya.MFnData.kString)
        td_attr.setHidden(False)
        td_attr.setKeyable(True)
        in_attrs.append(cls.DATA_LOCATION)

        m_attr = OpenMaya.MFnMatrixAttribute()
        cls.IN_MATRICES = m_attr.create("matrix", "mat")
        m_attr.setKeyable(True)
        m_attr.setArray(True)
        in_attrs.append(cls.IN_MATRICES)

        # Manage attributes
        for attribute in (in_attrs + out_attrs):
            cls.addAttribute(attribute)

        #   Set the attribute dependencies
        for out_attr in out_attrs:
            for in_attr in in_attrs:
                cls.attributeAffects(in_attr, out_attr)

    @classmethod
    def get_input_mesh(cls, data: OpenMaya.MDataBlock, idx: int) -> OpenMaya.MObject:
        """!@Brief Get deformer input mesh from input id."""
        input_handle = data.outputArrayValue(OpenMayaMPx.cvar.MPxGeometryFilter_input)
        input_handle.jumpToElement(idx)

        return input_handle.outputValue().child(OpenMayaMPx.cvar.MPxGeometryFilter_inputGeom).asMesh()

    def __load_models(self, data: OpenMaya.MDataBlock):
        """!@Brief Load models from the json file given."""
        path = data.inputValue(self.DATA_LOCATION).asString()
        log.info(f"Loading models from {path}")

        self._clear()
        data = self.__read_models(path)
        models = data[self.kModels]
        if not models:
            return

        for i, model in enumerate(models):
            self.models.append(self.__deserialize_model(i, data, model) if model else None)

    def __read_models(self, path: str) -> dict:
        data = dict()

        if not self.location_changed:
            return data
        if not os.path.exists(path):
            log.error(f"Could not find file {path} !")
            return data

        self.location_changed = False
        self.data_location = path
        with open(path, "r") as f:
            data = json.load(f)

        if self.kModels not in data:
            log.error("No models defined in data !")
            return data

        return data

    def __deserialize_model(self, model_ids: int, data: dict, model: dict) -> TFModel:
        vertices = data[self.kJointMap][model_ids]
        graph = Graph()
        with graph.as_default():
            session = Session()
            with session.as_default():
                meta = model.get(self.kMeta)
                root = model.get(self.kRoot)
                saver = tf.train.import_meta_graph(meta)
                saver.restore(session, tf.train.latest_checkpoint(root))

                return TFModel(graph=session.graph,
                               session=session,
                               input_tensor=session.graph.get_tensor_by_name(model[self.kInput]),
                               output_tensor=session.graph.get_tensor_by_name(model[self.kOutput]),
                               vertices=vertices)

    @classmethod
    def __get_envelope(cls, data: OpenMaya.MDataBlock) -> float:
        return data.inputValue(OpenMayaMPx.cvar.MPxGeometryFilter_envelope).asFloat()

    def __get_matrices(self, data: OpenMaya.MDataBlock, num_models: int) -> list:
        matrices = list()

        matrices_handle = data.inputArrayValue(self.IN_MATRICES)
        matrix_count = matrices_handle.elementCount()
        if matrix_count > num_models:
            log.error("More input joints than models !")
            return matrices

        for i in range(matrix_count):
            matrices_handle.jumpToElement(i)
            matrix_handle = matrices_handle.inputValue()
            matrices.append(np.array(maya_utils.array_from_matrix(matrix_handle.asMatrix())))

        return matrices

    @classmethod
    def __get_prediction(cls, model: TFModel, values: np.array) -> np.array:
        # Keras trains with the regular shape, but tensorflow expects the transposed version.
        array = np.array([[v] for v in values]).T

        # Set the graph and session, and guess the values.
        with model.graph.as_default():
            with model.session.as_default():
                results = model.session.run(model.output_tensor, feed_dict={model.input_tensor: array})
                prediction = results[0]

        return prediction

    def __get_deltas(self, mesh: OpenMaya.MObject, matrices: list) -> np.array:
        mesh_fn = OpenMaya.MFnMesh(mesh)
        deltas = np.zeros(3 * mesh_fn.numVertices())

        for i in range(len(matrices)):
            # Some joints don"t have a model in the json so skip them.
            model = self.models[i]
            if not model:
                continue

            prediction = self.__get_prediction(model, matrices[i])
            for j, vtx in enumerate(model.vertices):
                deltas[vtx * 3:(vtx * 3) + 3] = prediction[j * 3:(j * 3) + 3]

        return deltas

    def __apply_deltas(self, deltas: list, envelope: float,
                       iterator: OpenMaya.MItGeometry,
                       data: OpenMaya.MDataBlock, geom_id: int):
        while not iterator.isDone():
            index = iterator.index()
            pos = iterator.position()
            weight = self.weightValue(data, geom_id, index)

            delta = deltas[index * 3:(index * 3) + 3]
            delta = [d * envelope * weight for d in delta]
            pos.x += delta[0]
            pos.y += delta[1]
            pos.z += delta[2]

            iterator.setPosition(pos)
            iterator.next()

    def deform(self, data: OpenMaya.MDataBlock,
               iterator: OpenMaya.MItGeometry,
               matrix: OpenMaya.MMatrix, geom_id: int):
        if self.location_changed:
            self.__load_models(data)

        num_models = len(self.models)
        if num_models == 0:
            log.error("No model found !")
            return

        envelope = self.__get_envelope(data)
        matrices = self.__get_matrices(data, num_models)
        deltas = self.__get_deltas(self.get_input_mesh(data, geom_id), matrices)
        self.__apply_deltas(deltas, envelope, iterator, data, geom_id)

    # noinspection PyPep8Naming
    def preEvaluation(self, context, evaluation_node) -> None:
        """!@Brief Check if certain values have changed to cause a recache"""
        if evaluation_node.dirtyPlugExists(FDDADeformerNode.DATA_LOCATION):
            self.location_changed = True
        return super(FDDADeformerNode, self).preEvaluation(context, evaluation_node)

    # noinspection PyPep8Naming
    def setDependentsDirty(self, plug, plug_array) -> None:
        """!@Brief Check if certain values have changed to cause a recache"""
        if plug == FDDADeformerNode.DATA_LOCATION:
            self.location_changed = True
        return super(FDDADeformerNode, self).setDependentsDirty(plug, plug_array)


# noinspection PyPep8Naming
def initializePlugin(plugin):
    plugin = OpenMayaMPx.MFnPlugin(plugin, "QuanticDream", "1.0")
    try:
        plugin.registerNode(FDDADeformerNode.kNodeName,
                            FDDADeformerNode.kNodeID,
                            FDDADeformerNode.creator,
                            FDDADeformerNode.initialize,
                            OpenMayaMPx.MPxNode.kDeformerNode)
    except Exception:
        raise RuntimeError(f"Failed to register node: {FDDADeformerNode.kNodeName}")


# noinspection PyPep8Naming
def uninitializePlugin(plugin):
    plugin = OpenMayaMPx.MFnPlugin(plugin)

    try:
        plugin.deregisterNode(FDDADeformerNode.id)
    except Exception:
        raise RuntimeError(f"Failed to unregister node: {FDDADeformerNode.kNodeName}")