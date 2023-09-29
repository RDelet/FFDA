# coding=ascii

from maya import OpenMaya

import numpy as np

from fdda.core.logger import log
from fdda.maya.core import api_utils
from fdda.maya.core.skin import Skin
from fdda.maya.core.context import KeepCurrentFrame, DisableRefresh


class BaseData:

    def __init__(self, *args, **kwargs):
        pass
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"FDDA(class: {self.__class__.__name__})"


class SkinData(BaseData):

    def __init__(self):
        self.skin = Skin()
        self.weight_map = list()
        self.joint_map = list()
        self.n_verts = 0

    def clear(self):
        self.skin = Skin()
        self.weight_map = list()
        self.joint_map = list()
        self.n_verts = 0

    def get(self, mesh_path: OpenMaya.MDagPath):
        self.clear()

        self.skin = Skin.find(mesh_path)
        if not self.skin:
            raise RuntimeError(f"No skin cluster found on {mesh_path.fullPathName()} !")

        inf_count = self.skin.influences_count()
        weights = [self.skin.weights[i] for i in range(self.skin.weights.length())]
        self.weight_map = list()
        self.joint_map = [list() for _ in range(inf_count)]
        self.n_verts = OpenMaya.MFnMesh(self.skin.shape).numVertices()

        for vtx in range(OpenMaya.MFnMesh(self.skin.shape).numVertices()):
            vtx_weights = weights[vtx * inf_count: (vtx * inf_count) + inf_count]
            i_max = np.argmax(np.array(vtx_weights))
            self.weight_map.append(vtx_weights[i_max])
            self.joint_map[i_max].append(vtx)


class MeshData(BaseData):

    def __init__(self):
        self.frame_data = dict()
        self.skin_data = SkinData()

    def clear(self):
        self.frame_data = dict()
        self.skin_data.clear()

    @KeepCurrentFrame()
    @DisableRefresh()
    def get(self, source: OpenMaya.MDagPath, destination: OpenMaya.MDagPath, start: float = None, end: float = None):
        """!@Brief: Build data from a maya scene. Input: Joint quaternion and translation vector and delta between
        source and destination object."""
        self.clear()
        self.skin_data.get(destination)

        inf_names = self.skin_data.skin.influences_names
        self.frame_data = {jnt: list() for jnt in inf_names}

        for frame in api_utils.time_line_range(start=start, end=end):
            log.info(f"Processing frame: {frame}")
            api_utils.set_current_time(frame)

            source_pts = api_utils.get_points(source)
            destination_pts = api_utils.get_points(destination)
            if source_pts.length() != destination_pts.length():
                raise RuntimeError("Mismatch number of points between source and destination mesh !")

            for jnt_id, vertices in enumerate(self.skin_data.joint_map):
                jnt = inf_names[jnt_id]

                # Conversion homogenous transformation matrix (4x4) to quaternion and translation vector
                local_mat = api_utils.matrix_of(jnt, world=False)
                transform = OpenMaya.MTransformationMatrix(local_mat)
                q = transform.rotation()

                data = [q.x, q.y, q.z, q.w]

                for vtx_id in vertices:
                    delta = source_pts[vtx_id] - destination_pts[vtx_id]
                    data.extend([delta.x, delta.y, delta.z])
                self.frame_data[jnt].append(data)