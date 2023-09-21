# coding=ascii

from typing import Union

from maya import OpenMaya


kInputName = "input_data"
kOutputName = "output_data"
kExtension = "json"
kJsonIndent = 4

kdagType = Union[str, OpenMaya.MObject, OpenMaya.MDagPath]
kdepType = Union[str, OpenMaya.MObject]

kInputHeading = ["qx", "qy", "qz", "qw"]
