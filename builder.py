# coding=ascii
import copy
import csv
import json
import os

from maya import cmds, OpenMaya

from fdda.logger import log
from fdda import context, utils as maya_utils
from fdda.skin import Skin
from fdda.fddaDeformerNode import FDDADeformerNode
from fdda import training, constant as cst
from fdda.training import Settings


class SkinData:

    def __init__(self):
        self.skin = Skin()
        self.weight_map = list()
        self.joint_map = list()

    def clear(self):
        self.skin = Skin()
        self.weight_map = list()
        self.joint_map = list()

    def get(self, mesh_path: OpenMaya.MDagPath):
        self.clear()

        skin_node = Skin.find(mesh_path)
        if not skin_node:
            raise RuntimeError(f"No skin cluster found on {mesh_path.fullPathName()} !")
        self.skin = Skin(skin_node)

        inf_count = self.skin.influences_count()
        weights = [self.skin.weights[i] for i in range(self.skin.weights.length())]
        self.weight_map = list()
        self.joint_map = [list() for _ in range(inf_count)]
        for vtx in range(OpenMaya.MFnMesh(self.skin.shape).numVertices()):
            vtx_weights = weights[vtx * inf_count: (vtx * inf_count) + inf_count]
            for i, weight in enumerate(vtx_weights):
                if weight > 0:
                    self.weight_map.append(weight)
                    self.joint_map[i].append(vtx)


class MeshData:

    def __init__(self):
        self.frame_data = dict()
        self.skin_data = SkinData()

    def clear(self):
        self.frame_data = dict()
        self.skin_data.clear()

    def get(self, target: OpenMaya.MDagPath, destination: OpenMaya.MDagPath, start: float = None, end: float = None):
        self.clear()
        self.skin_data.get(destination)

        inf_names = self.skin_data.skin.influences_names
        self.frame_data = {jnt: list() for jnt in inf_names}

        with context.KeepCurrentFrame():
            for frame in maya_utils.time_line_range(start=start, end=end):
                log.info(f"Processing frame: {frame}")
                maya_utils.set_current_time(frame)

                target_pts = maya_utils.get_points(target)
                destination_pts = maya_utils.get_points(destination)
                if target_pts.length() != destination_pts.length():
                    raise RuntimeError("Mismatch number of points between target and destination mesh !")

                for jnt_id, vertices in enumerate(self.skin_data.joint_map):
                    jnt = inf_names[jnt_id]
                    data = maya_utils.array_from_matrix(maya_utils.matrix_of(jnt, world=False))
                    for vtx_id in vertices:
                        delta = target_pts[vtx_id] - destination_pts[vtx_id]
                        data.extend([delta.x, delta.y, delta.z])
                    self.frame_data[jnt].append(data)


class Builder(object):

    def __init__(self, target: cst.kdagType = None, destination: cst.kdagType = None, file: str = None):
        self._target = self.__get_node(target)
        self._destination = self.__get_node(destination)
        self._file = file
        self._data = None
        self._deformer = None

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(file: {self._file}, target: {self.target}, destination: {self.destination})"

    @staticmethod
    def __get_node(n):
        if isinstance(n, (str, OpenMaya.MObject)):
            if isinstance(n, str):
                n = maya_utils.get_object(n)
            if not n.hasFn(OpenMaya.MFn.kDagNode):
                return n
            return maya_utils.get_path(n)
        elif isinstance(n, OpenMaya.MDagPath):
            return n
        else:
            raise RuntimeError(f"Argument must be a str, MObject or MDagPath not {type(n)} !")

    def clear(self):
        self._target = None
        self._destination = None
        self._file = None
        self._deformer = None

    @property
    def file(self) -> str:
        return self._file

    @file.setter
    def file(self, value):
        if not os.path.exists(value):
            raise RuntimeError(f"Path {value} does not exists !")

        self._file = value
        with open(self._file, 'r') as stream:
            self._data = json.load(stream)

        if self._deformer is not None:
            deformer_name = maya_utils.name_of(self._deformer)
            cmds.setAttr(f"{deformer_name}.{FDDADeformerNode.kTrainingDataLong}",
                         self._file, type='string')

    @property
    def target(self) -> OpenMaya.MDagPath:
        return self._target

    @target.setter
    def target(self, value: cst.kdagType):
        self._target = self.__get_node(value)

    @property
    def destination(self) -> OpenMaya.MDagPath:
        return self._destination

    @destination.setter
    def destination(self, value: cst.kdagType):
        self._destination = self.__get_node(value)

    @property
    def deformer(self) -> OpenMaya.MDagPath:
        return self._deformer

    @deformer.setter
    def deformer(self, value: cst.kdepType):
        self._deformer = self.__get_node(value)

    @property
    def data(self) -> dict:
        if not self.file:
            raise RuntimeError(f"No file set !")
        with open(self.file, 'r') as f:
            return json.load(f)

    @staticmethod
    def load_plugin():
        pass

    def build_models(self, out_dir: str, bind: bool = False, settings: Settings = Settings.default()):
        """!Brief Build models from meshes.

        @out_dir: Model output directory.
        @bind: Bind deformer after train.
        """
        try:
            input_path = self._data_acquisition(out_dir=out_dir)
            input_dir, _ = os.path.split(input_path)
            self._file = os.path.normpath(os.path.join(input_dir, f"{cst.kOutputName}.{cst.kExtension}"))
        except Exception as e:
            log.debug(e)
            raise RuntimeError("Error on get data between {target} and {destination} !")

        try:
            training_data = training.train(out_dir, settings)
        except Exception as e:
            log.debug(e)
            raise RuntimeError("Error on train model between {target} and {destination} !")

        if bind:
            self._bind()

        return training_data

    def _bind(self):
        dst_name = maya_utils.name_of(self.destination)
        try:
            self.deformer = cmds.deformer(dst_name, type=FDDADeformerNode.kNodeName)[0]
        except Exception as e:
            log.debug(e)
            raise RuntimeError(f"Error on bind deformer on {dst_name}!")

        self.file = self.file

        deformer_name = maya_utils.name_of(self.deformer)
        joint_names = self._data.get('joint_names', list())
        for i, jnt in enumerate(joint_names):
            cmds.connectAttr(f"{jnt}.matrix", f"{deformer_name}.matrix[{i}]")

    @classmethod
    def bind(cls, destination: cst.kdagType, file: str):
        """!@Brief Bind FDDA deformer."""
        maya_utils.go_to_start_frame()
        fdda = Builder(destination=destination, file=file)
        fdda._bind()

        return fdda

    def _data_acquisition(self, out_dir: str = None,
                          start: float = None, end: float = None) -> str:
        """!@Brief Write out data for the machine learning algorithm to train from.
        @param out_dir: The directory to write to. If no directory is provided, uses training directory.
        @param start: The start frame to write from.
        @param end: The end frame to write to
        @return: The path to the written data.
        """
        if self.target is None:
            raise RuntimeError("No target set !")
        if self.destination is None:
            raise RuntimeError("No destination set !")
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        mesh_data = MeshData()
        mesh_data.get(self.target, self.destination, start=start, end=end)
        skin_data = mesh_data.skin_data

        data = {"input_fields": cst.kMatrixHeading,
                "csv_files": self.__dump_csv(mesh_data, skin_data, out_dir),
                "joint_names": skin_data.skin.influences_names,
                "joint_indexes": [i for i in skin_data.skin.influences_ids],
                "weights": skin_data.weight_map,
                "joint_map": skin_data.joint_map}

        return self.__dump_data(data, out_dir)

    @classmethod
    def __dump_csv(cls, mesh_data: MeshData, skin_data: SkinData, out_dir: str) -> list:
        csv_files = list()

        skin_inf = skin_data.skin.influences_names
        for jnt in skin_inf:
            data = mesh_data.frame_data[jnt]

            heading = copy.copy(cst.kMatrixHeading)
            for v in skin_data.joint_map[skin_inf.index(jnt)]:
                heading.extend([f"vtx{v}x", f"vtx{v}y", f"vtx{v}z"])

            file_name = f"{jnt.split('|')[-1]}.csv"
            file_path = os.path.join(out_dir, file_name)
            log.info(f"Wrote data for {jnt} to {file_path}")

            with open(file_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(heading)
                writer.writerows(data)

            csv_files.append(file_path)

        return csv_files

    @classmethod
    def __dump_data(cls, data: dict, output_directory: str) -> str:
        file_path = os.path.normpath(os.path.join(output_directory, f"{cst.kInputName}.{cst.kExtension}"))
        log.info(f"Wrote Weight Map to {file_path}")

        try:
            with open(file_path, 'w') as stream:
                json.dump(data, stream, indent=cst.kJsonIndent)
        except Exception as e:
            log.debug(e)
            raise RecursionError("Error on dump data !")

        return file_path
