import os

import fdda
from fdda.logger import log
from fdda.architecture import Activation, Settings

from maya import cmds


def find_mesh(node):
    if cmds.nodeType(node) == "transform":
        shapes = cmds.listRelatives(node, shapes=True, fullPath=True)
        if not shapes:
            raise RuntimeError(f"No shape found under node !")
        meshes = [x for x in shapes if cmds.nodeType(x) == "mesh"]
        if not meshes:
            raise RuntimeError(f"No mesh found under node !")
        return meshes[0]
    elif not cmds.nodeType(node) == "mesh":
        raise RuntimeError("Only mesh is accepted !")

    return node


def retrieve_skin(mesh):
    history = cmds.listHistory(mesh) or []
    if not history:
        raise RuntimeError(f"No histroy found on {mesh} !")
    skin = [x for x in history if cmds.nodeType(x) == "skinCluster"]
    if not history:
        raise RuntimeError(f"No skin found on {mesh} !")
    elif len(skin) > 1:
         raise RuntimeError(f"Multi skin cluster foudn on {mesh} !")
    
    return skin[0]

def retrieve_influences(mesh):
    skin = retrieve_skin(mesh)
    influences = cmds.skinCluster(skin, query=True, influence=True)
    if not influences:
        raise RuntimeError("No influences found on skin {skin} !")

    return influences


def get_steps(angle_max=360, step_count=20):
    angle_max = 360
    step_count = 20
    step = angle_max / step_count

    return [step * i for i in range(step_count + 1)]


def build_pose(mesh, step_count=20, angle_max=360):
    
    influences = retrieve_influences(mesh)
    num_frame = step_count * 3 * len(influences)
    steps = get_steps(angle_max=angle_max, step_count=step_count)
    cmds.playbackOptions(minTime=0, maxTime=num_frame,
                         animationStartTime=0, animationEndTime=num_frame)

    i = 0
    [cmds.setAttr(f"{x}.rotate", *[0, 0, 0]) for x in influences]
    for inf in influences:
        for axis in "XYZ":
            for step in steps:
                cmds.currentTime(i)
                cmds.setAttr(f"{inf}.rotate{axis}", step)
                cmds.setKeyframe(inf)
                i += 1
            cmds.setAttr(f"{inf}.rotate", *[0, 0, 0])


def train(source, target):
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
    settings.rate = 1e-3
    settings.layers = 3
    settings.epochs = 200
    settings.activation = Activation.kRelu
    fdda.build_models(selected[0], selected[1], output_path, settings=settings, bind=True)


selected = cmds.ls(selection=True, long=True)
if not selected or len(selected) != 2:
    raise RuntimeError("Select source and target mesh !")


source = find_mesh(selected[0])
target = find_mesh(selected[1])
build_pose(target)
train(source, target)
