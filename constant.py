# coding=ascii

from typing import Union

from maya import OpenMaya

kInputName = "input_data"
kOutputName = "output_data"
kExtension = "json"
kJsonIndent = 4

kNodeType = Union[str, OpenMaya.MObject, OpenMaya.MDagPath]

kMatrixHeading = ["m00", "m01", "m02", "m03",
                  "m10", "m11", "m12", "m13",
                  "m20", "m21", "m22", "m23",
                  "m30", "m31", "m32", "m33"]
