"""
# -----------------------
# Script pour Maya:
# -----------------------
import sys

sys.path.insert(0, r"D:\RDE_DATA\Work")

from maya import cmds, OpenMaya

from fdda.maya import bind, train, generate_pose
from fdda.training.PyTorch.settings import Settings


selected = cmds.ls(selection=True, long=True)
if len(selected) != 2:
    raise RuntimeError("Selected Source and Destination !")
source, destination = selected

settings = Settings.default()
settings.split = 0.1
settings.units = 256
settings.device = Settings.kGpu

output_path = train(source, destination, settings, build_pose=True, num_pose=40)
bind(destination, output_path)
"""

import os

from maya import cmds

from fdda import kBipedLimitsPath
from fdda.core.logger import log
from fdda.maya.core import api_utils
from fdda.maya.core import constant as cst
from fdda.maya.poseGenerator import PoseGenerator
from fdda.maya.builder import Builder
from fdda.maya.binder import Binder
from fdda.training.PyTorch.training import build_models
from fdda.training.PyTorch.settings import Settings



_directory = os.path.split(__file__)[0]


def get_path_from_scene() -> str:
    scene_name = cmds.file(query=True, sceneName=True)
    if not scene_name:
        raise RuntimeError("Scene must be save before train !")

    directory_path, file_name = os.path.split(scene_name)
    output_path = os.path.normpath(os.path.join(directory_path, file_name.split(".")[0]))
    if not os.path.exists(output_path):
        os.mkdir(output_path)
        log.info(f"Create directory: {output_path}")
    
    return output_path

def bind(node: cst.kdagType, input_directory: str):
    """ @!Brief Bind FDDA deformer."""
    api_utils.go_to_start_frame()
    binder = Binder(destination=node, input_directory=input_directory)
    binder.bind()


def generate_pose(node: str, num_pose: int = 40, data_path: str = kBipedLimitsPath):
    pose_generator = PoseGenerator(node)
    pose_generator.generate(num_pose)


def train(source: str, destination: str,
          settings: Settings = Settings.default(),
          build_pose: bool = True, num_pose: int = 40) -> str:
    output_path = get_path_from_scene()

    if build_pose:
        generate_pose(source, num_pose=num_pose)

    data_builder = Builder(source, destination)
    data_builder.do(output_path)

    build_models(input_directory=output_path, settings=settings, mode=True, normalized=True, debug=True)

    return output_path


def load_node():
    node_path = os.path.normpath(os.path.join(_directory, "nodes/Proto", "fddaDeformerNode.py"))
    if not cmds.pluginInfo(node_path, query=True, loaded=True):
        cmds.loadPlugin(node_path)


try:
    load_node()
except Exception as e:
    log.debug(e)
    raise RuntimeError("Error on load FDDA plugin !")
