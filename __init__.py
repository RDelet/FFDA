"""
import os

import fdda
from fdda.logger import log
from fdda.architecture import Activation, Settings


# Activate pycharm debug (only for pycharm pro)
debug_with_pycharm = False
if debug_with_pycharm:
    from fdda import pycharm_debug
    pycharm_debug.connect(port=50016)

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
    raise RuntimeError("Selected Target and Destination !")

settings = Settings.default()
settings.rate = 1e-4
settings.layers = 6
settings.epochs = 400
settings.activation = Activation.kRelu
fdda.build_models(selected[0], selected[1], output_path, settings=settings, bind=True)
"""

import os

from maya import cmds

from fdda.architecture import Settings
from fdda.builder import Builder
from fdda.logger import log

_directory = os.path.split(__file__)[0]


def build_models(target: str, destination: str, output_directory: str,
                 bind: bool = False, settings: Settings = Settings.default()):
    fdda_builder = Builder(target, destination)
    fdda_builder.build_models(output_directory, bind=bind, settings=settings)


def load_node():
    node_path = os.path.normpath(os.path.join(_directory, "fddaDeformerNode.py"))
    if not cmds.pluginInfo(node_path, query=True, loaded=True):
        cmds.loadPlugin(node_path)


try:
    load_node()
except Exception as e:
    log.debug(e)
    raise RuntimeError("Error on load FDDA plugin !")
