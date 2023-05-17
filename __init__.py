"""
import os
import fdda

fdda.load_node()

debug_with_pycharm = False
if debug_with_pycharm:
    from fdda import pycharm_debug
    pycharm_debug.connect(port=50016)

scene_name = cmds.file(query=True, sceneName=True)
if not scene_name:
    raise RuntimeError("Scene must be save before train !")
directory_path, file_name = os.path.split(scene_name)
output_path = os.path.normpath(os.path.join(directory_path, file_name.split(".")[0]))
if not os.path.exists(output_path):
    os.mkdir(output_path)

fdda.build_models("Tube", "Tube1", directory_path)
"""

import os

from maya import cmds

from fdda.builder import Builder
from fdda import logger

_directory = os.path.split(__file__)[0]


def build_models(target: str, destination: str, output_directory: str):
    fdda_builder = Builder(target, destination)
    fdda_builder.build_models(output_directory)


def load_node():
    node_path = os.path.normpath(os.path.join(_directory, "fddaDeformerNode.py"))
    if not cmds.pluginInfo(node_path, query=True, loaded=True):
        cmds.loadPlugin(node_path)
