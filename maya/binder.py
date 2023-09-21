# coding=ascii
import os
import json

from maya import cmds, OpenMaya

from fdda.core.logger import log
from fdda.core import api_utils, constant as cst
from fdda.maya.nodes.fddaDeformerNode import FDDADeformerNode
from fdda.core import api_utils


class Binder(object):

    def __init__(self, destination: cst.kdagType, input_directory: str):
        self._destination = api_utils.get_node(destination)
        self._file = os.path.normpath(os.path.join(input_directory, f"{cst.kOutputName}.{cst.kExtension}"))
        self._data = None
        self._deformer = None

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"(class: {self.__class__.__name__}, file: {self._file}, destination: {self._destination})"

    def clear(self):
        self._destination = None
        self._file = None
        self._data = None
        self._deformer = None

    @property
    def destination(self) -> OpenMaya.MDagPath:
        return self._destination

    @destination.setter
    def destination(self, value: cst.kdagType):
        self._destination = api_utils.get_node(value)

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
            deformer_name = api_utils.name(self._deformer)
            cmds.setAttr(f"{deformer_name}.{FDDADeformerNode.kTrainingDataLong}",
                         self._file, type='string')

    @property
    def deformer(self) -> OpenMaya.MDagPath:
        return self._deformer

    @deformer.setter
    def deformer(self, value: cst.kdepType):
        self._deformer = api_utils.get_node(value)

    @property
    def data(self) -> dict:
        if not self.file:
            raise RuntimeError(f"No file set !")
        with open(self.file, 'r') as f:
            return json.load(f)

    def bind(self):
        dst_name = api_utils.name(self.destination)
        try:
            self.deformer = cmds.deformer(dst_name, type=FDDADeformerNode.kNodeName)[0]
        except Exception as e:
            log.debug(e)
            raise RuntimeError(f"Error on bind deformer on {dst_name}!")
        
        cmds.setAttr(f"{api_utils.name(self.deformer)}.trainingData", self._file, type="string")

        deformer_name = api_utils.name(self.deformer)
        joint_names = self.data.get('joint_names', list())
        for i, jnt in enumerate(joint_names):
            cmds.connectAttr(f"{jnt}.matrix ", f"{deformer_name}.matrix[{i}]")
