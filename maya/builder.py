# coding=ascii

import copy
import csv
import json
import os
import traceback

from maya import OpenMaya

from fdda.core import constant as cst
from fdda.core.logger import log
from fdda.maya.core import api_utils
from fdda.maya.core.data import SkinData, MeshData
from fdda.maya.core import constant as maya_cst


class Builder(object):

    def __init__(self, source: maya_cst.kdagType = None, destination: maya_cst.kdagType = None):
        self._source = api_utils.get_node(source)
        self._destination = api_utils.get_node(destination)
        self._data = None

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        src_name = api_utils.name(self.source)
        dst_name = api_utils.name(self.destination)
        return f"(class: {self.__class__.__name__}, source: {src_name}, destination: {dst_name})"

    def clear(self):
        self._source = None
        self._destination = None
        self._data = None

    @property
    def source(self) -> OpenMaya.MDagPath:
        return self._source

    @source.setter
    def source(self, value: maya_cst.kdagType):
        self._source = api_utils.get_node(value)

    @property
    def destination(self) -> OpenMaya.MDagPath:
        return self._destination

    @destination.setter
    def destination(self, value: maya_cst.kdagType):
        self._destination = api_utils.get_node(value)

    def do(self, output_dir: str,
                   start: float = None, end: float = None) -> str:
        """!Brief Build models from meshes."""
        try:
            return self._data_acquisition(out_dir=output_dir, start=start, end=end)
        except Exception:
            log.debug(traceback.format_exc())
            raise RuntimeError("Error on get data !")

    def _data_acquisition(self, out_dir: str = None,
                          start: float = None, end: float = None) -> str:
        """!@Brief Write out data for the machine learning algorithm to train from."""
        if self.source is None:
            raise RuntimeError("No source set !")
        if self.destination is None:
            raise RuntimeError("No destination set !")
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        mesh_data = MeshData()
        mesh_data.get(self.source, self.destination, start=start, end=end)
        skin_data = mesh_data.skin_data

        data = {"input_fields": cst.kInputHeading,
                "csv_files": self.__dump_csv(mesh_data, skin_data, out_dir),
                "joint_names": skin_data.skin.influences_names,
                "joint_indexes": [i for i in skin_data.skin.influences_ids],
                "weights": skin_data.weight_map,
                "joint_map": skin_data.joint_map,
                "n_vertices": skin_data.n_verts}

        return self.__dump_data(data, out_dir)

    @classmethod
    def __dump_csv(cls, mesh_data: MeshData, skin_data: SkinData, out_dir: str) -> list:
        csv_files = list()

        skin_inf = skin_data.skin.influences_names
        for jnt in skin_inf:
            data = mesh_data.frame_data[jnt]
            heading = copy.copy(cst.kInputHeading)

            # Repeat the heading two times because we stock the source mesh vertices & the destination mesh vertices.
            for v in skin_data.joint_map[skin_inf.index(jnt)]:
                heading.extend([f"vtx{v}x", f"vtx{v}y", f"vtx{v}z"])

            file_name = f"{jnt.split('|')[-1].split(':')[-1]}.csv"
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
        except Exception:
            log.debug(traceback.format_exc())
            raise RecursionError("Error on dump data !")

        return file_path
