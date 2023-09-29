# coding=ascii

import numpy as np

from maya import OpenMaya, OpenMayaMPx

from fdda.core.logger import log
from fdda.training.PyTorch.loader import Loader
from fdda.training.PyTorch.architecture import get_prediction
from fdda.maya.core import constant as maya_cst


class FDDADeformerNode(OpenMayaMPx.MPxDeformerNode):

    kNodeName = maya_cst.kNodeName
    kNodeID = OpenMaya.MTypeId(0x0012d5c1)

    DATA_LOCATION = OpenMaya.MObject()
    IN_MATRICES = OpenMaya.MObject()

    def __init__(self, *args):
        super(FDDADeformerNode, self).__init__(*args)

        self._loader = Loader()
        self._location_changed = True
  
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"FDDA(class: {self.__class__.__name__})"

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
    def __get_envelope(cls, data: OpenMaya.MDataBlock) -> float:
        return data.inputValue(OpenMayaMPx.cvar.MPxGeometryFilter_envelope).asFloat()

    def __get_matrices(self, data: OpenMaya.MDataBlock, num_models: int) -> list:
        matrices = list()

        matrices_handle = data.inputArrayValue(self.IN_MATRICES)
        matrix_count = matrices_handle.elementCount()
        # In local mode, we need to have the same number of joints and models.
        if matrix_count > num_models and not self._loader.global_mode:
            log.error("More input joints than models ! ({} joints and {} models.".format(matrix_count, num_models))
            return matrices

        for i in range(matrix_count):
            matrices_handle.jumpToElement(i)
            matrix_handle = matrices_handle.inputValue()

            # Conversion homogenous transformation matrix (4x4) to quaternion and translation vector
            transform = OpenMaya.MTransformationMatrix(matrix_handle.asMatrix())
            q = transform.rotation()
            matrices.append(np.array([q.x, q.y, q.z, q.w], dtype=np.float32))

        if self._loader.global_mode:
            matrices = [np.concatenate(matrices)]

        return matrices

    def __get_deltas(self, iterator: OpenMaya.MItGeometry, matrices: list) -> np.array:
        deltas = np.zeros(3 * iterator.count())

        for i in range(len(matrices)):
            # Some joints don"t have a model in the json so skip them.
            model = self._loader.models[i]
            mean = self._loader.means[i]
            std = self._loader.stds[i]
            if not model:
                continue

            prediction = get_prediction(model, matrices[i], mean, std,
                                        normalized=self._loader.normalized,
                                        device=self._loader.device)

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
            file_path = data.inputValue(self.DATA_LOCATION).asString()
            if not self._loader.load(file_path):
                return
            self.location_changed = False

        if self._loader.model_count == 0:
            log.error("No model found !")
            return

        envelope = self.__get_envelope(data)
        matrices = self.__get_matrices(data, self._loader.model_count)
        deltas = self.__get_deltas(iterator, matrices)
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
        plugin.deregisterNode(FDDADeformerNode.kNodeID)
    except Exception:
        raise RuntimeError(f"Failed to unregister node: {FDDADeformerNode.kNodeName}")
