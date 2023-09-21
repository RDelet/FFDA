"""
# -----------------------
# Script pour Maya:
# -----------------------

import imp
import os
import sys

sys.path.insert(0, r"D:\RDE_DATA\Work")

from fdda import maya
from fdda.core.logger import log
from fdda.maya import bind
from fdda.maya.builder import Builder
from fdda.maya.poseGenerator import PoseGenerator
from fdda.training.PyTorch.training import build_models
from fdda.training.PyTorch.architecture import Activation
from fdda.training.PyTorch.settings import Settings


generatePose = False


# Get output directory
scene_name = cmds.file(query=True, sceneName=True)
if not scene_name:
    raise RuntimeError("Scene must be save before train !")

directory_path, file_name = os.path.split(scene_name)
output_path = os.path.normpath(os.path.join(directory_path, file_name.split(".")[0]))
if not os.path.exists(output_path):
    os.mkdir(output_path)
    log.info(f"Create directory: {output_path}")

# Train
selected = cmds.ls(selection=True, long=True)
if len(selected) != 2:
    raise RuntimeError("Selected Source and Destination !")

if generatePose:
    pose_generator = PoseGenerator(selected[0])
    pose_generator.generate(40)

# Build data from source and destination meshes.
data_builder = Builder(*selected)
data_builder.do(output_path)

settings = Settings.default()
settings.rate = 1e-3
settings.layers = 4
settings.epochs = 800
settings.activation = Activation.kElu
settings.split = 0.1
settings.units = 256
settings.batch_size = 128
settings.device = Settings.kCpu

build_models(input_directory=output_path, settings=settings, mode=True, normalized=True, debug=True)

bind(selected[1], output_path)
"""

import os

from maya import cmds

from fdda.core import constant as cst
from fdda.core.logger import log
from fdda.core import api_utils
from fdda.maya.binder import Binder


_directory = os.path.split(__file__)[0]


def bind(node: cst.kdagType, input_directory: str):
    """ @!Brief Bind FDDA deformer."""
    api_utils.go_to_start_frame()
    binder = Binder(destination=node, input_directory=input_directory)
    binder.bind()


def load_node():
    node_path = os.path.normpath(os.path.join(_directory, "nodes", "fddaDeformerNode.py"))
    if not cmds.pluginInfo(node_path, query=True, loaded=True):
        cmds.loadPlugin(node_path)


try:
    load_node()
except Exception as e:
    log.debug(e)
    raise RuntimeError("Error on load FDDA plugin !")
