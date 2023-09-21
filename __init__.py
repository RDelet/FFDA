"""
# -----------------------
# Script pour Maya:
# -----------------------

import os

import fdda
from fdda.core.logger import log
from fdda.maya.builder import Builder

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

# Build data from source and destination meshes.
data_builder = Builder(*selected)
data_builder.do(output_path)

fdda.bind(dst=destination, input_directory=output_path)
"""
