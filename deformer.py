# coding=ascii
from typing import Union

from maya import cmds, OpenMaya, OpenMayaAnim

from fdda import utils as maya_utils


class Deformer(object):

    def __init__(self, node: Union[str, OpenMaya.MObject] = None):
        self._object = None
        self.mfn = None
        self.shape = None

        if node:
            self.__get(node)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self):
        return "{0}(Deformer: {1}, Shape: {2})".format(self.__class__.__name__,
                                                       self.deformer_name,
                                                       self.shape_name)

    @property
    def object(self) -> OpenMaya.MObject:
        return self._object

    @object.setter
    def object(self, value: Union[str, OpenMaya.MObject]):
        self.__get(value)

    def __get_shape(self):
        output_geom = self.outputs_geometry()
        if output_geom.length() == 0:
            raise RuntimeError(f"No output shape found on {maya_utils.name_of(self.object)}")
        elif output_geom.length() > 1:
            raise RuntimeError(f"Multi shape found on {maya_utils.name_of(self.object)}")

        return self.outputs_geometry()[0]

    @property
    def deformer_name(self) -> str:
        return maya_utils.name_of(self.object) if self.object else ""
    
    def shape_name(self) -> str:
        return maya_utils.name_of(self.shape) if self.shape else ""

    def __get(self, node):
        if isinstance(node, str):
            node = maya_utils.get_object(node)

        self._object = node
        self.mfn = OpenMayaAnim.MFnGeometryFilter(node)
        self.shape = self.__get_shape()

    def outputs_geometry(self) -> OpenMaya.MObjectArray:
        output = OpenMaya.MObjectArray()
        self.mfn.getOutputGeometry(output)

        # It's possible "getOutputGeometry" don't return shape.
        # If no shape found check connection
        if output.length() == 0:
            out_geom_plug = self.mfn.findPlug("outputGeometry", False)
            out_plugs = OpenMaya.MPlugArray()
            out_geom_plug.destinations(out_plugs)
            for i in range(out_plugs.length()):
                output.append(out_plugs[i].node())

        return output

    def inputs_geometry(self) -> OpenMaya.MObjectArray:
        output = OpenMaya.MObjectArray()
        self.mfn.getInputGeometry(output)

        return output

    @classmethod
    def is_deformer(cls, node: OpenMaya.MObject):
        if isinstance(node, str):
            node = maya_utils.get_object(node)

        return node.hasFn(OpenMaya.MFn.kGeometryFilt)

    @classmethod
    def _find(cls, node: Union[str, OpenMaya.MObject, OpenMaya.MDagPath],
              mfn_type: int) -> Union[OpenMaya.MObject, OpenMaya.MObjectArray, None]:
        if isinstance(node, str):
            node = maya_utils.get_object(node)
        # If node is transform, retrieve shape
        node_to_parse = node
        if node.hasFn(OpenMaya.MFn.kTransform):
            mfn_node = OpenMaya.MFnTransform(node)
            for i in range(mfn_node.childCount()):
                child = mfn_node.child(i)
                if child.hasFn(OpenMaya.MFn.kShape):
                    child_name = maya_utils.name_of(child)
                    if cmds.getAttr(f"{child_name}.intermediateObject"):
                        continue
                    node_to_parse = child
                    break
        # Parse graph
        iterator = maya_utils.dependency_iterator_from(node_to_parse, mfn_type)
        output = OpenMaya.MObjectArray()
        while not iterator.isDone():
            output.append(iterator.currentItem())
            iterator.next()

        if output.length() == 1:
            return output[0]
        else:
            return output
