import math
from typing import Union

from maya import cmds, OpenMaya, OpenMayaAnim


_msl = OpenMaya.MSelectionList()
_maya_node = Union[str, OpenMaya.MObject, OpenMaya.MDagPath]


def get_object(n: str) -> OpenMaya.MObject:
    try:
        _msl.clear()
        _msl.add(n)
        mo = OpenMaya.MObject()
        _msl.getDependNode(0, mo)
        return mo
    except RuntimeError:
        if cmds.ls(n):
            raise RuntimeError(f"Multi node found for {n} !")
        raise RuntimeError(f"Node {n} does not exist !")


def get_path(n: Union[str, OpenMaya.MObject]) -> OpenMaya.MDagPath:

    if isinstance(n, str):
        try:
            _msl.clear()
            _msl.add(n)
            dp = OpenMaya.MDagPath()
            _msl.getDagPath(0, dp)
            return dp
        except RuntimeError:
            if cmds.ls(n):
                raise RuntimeError(f"Multi node found for {n} !")
            raise RuntimeError(f"Node {n} does not exist !")
    elif isinstance(n, OpenMaya.MObject):
        try:
            if n.isNull():
                raise RuntimeError("Object given is null !")
            moh = OpenMaya.MObjectHandle(n)
            if not moh.isValid() or not moh.isAlive():
                raise RuntimeError("Object given is not valid !")
            dp = OpenMaya.MDagPath()
            OpenMaya.MDagPath.getAPathTo(n, dp)
            return dp
        except RuntimeError:
            raise RuntimeError("Error on get path from MObject !")
    else:
        raise TypeError(f"Argument need to be str or MObject not {type(n)} !")


def name_of(node: Union[OpenMaya.MObject, OpenMaya.MDagPath],
            full: bool = True, namespace: bool = True):
    if isinstance(node, OpenMaya.MDagPath):
        return node.fullPathName()
    elif isinstance(node, OpenMaya.MPlug):
        return f"{name_of(node.node())}.{OpenMaya.MFnAttribute(node.attribute()).name()}"
    elif isinstance(node, OpenMaya.MObject):
        if not node.hasFn(OpenMaya.MFn.kDagNode) or not full:
            s_node = OpenMaya.MFnDependencyNode(node).name()
        else:
            s_node = OpenMaya.MFnDagNode(node).fullPathName()
        return s_node if namespace is True else s_node.split(":")[-1]
    else:
        raise TypeError(f"Argument must be a MObject or MDagPath not {type(node)}")


def dependency_iterator_from(node: _maya_node, mfn_type: int,
                             direction: int = OpenMaya.MItDependencyGraph.kUpstream,
                             traversal: int = OpenMaya.MItDependencyGraph.kDepthFirst,
                             level: int = OpenMaya.MItDependencyGraph.kNodeLevel) -> OpenMaya.MItDependencyGraph:
    if isinstance(node, str):
        node = get_object(node)
    if isinstance(node, OpenMaya.MDagPath):
        node = node.node()

    return OpenMaya.MItDependencyGraph(node, mfn_type, direction, traversal, level)


def matrix_of(node: _maya_node,
              exclusive: bool = False, inverse: bool = False, world: bool = True,
              time: OpenMaya.MTime = None) -> OpenMaya.MMatrix:
    if isinstance(node, (str, OpenMaya.MObject)):
        node = get_path(node)

    if time is not None:
        om_context = OpenMaya.MDGContext(time)
        om_context_guard = OpenMaya.MDGContextGuard(om_context)

    if world:
        if inverse:
            return node.exclusiveMatrixInverse() if exclusive else node.inclusiveMatrixInverse()
        return node.exclusiveMatrix() if exclusive else node.inclusiveMatrix()
    else:
        mfn = OpenMaya.MFnTransform(node)
        return mfn.transformation().asMatrixInverse() if inverse else mfn.transformation().asMatrix()


def array_from_matrix(matrix: OpenMaya.MMatrix) -> list:
    """!@Brief Transform maya matrix to float array."""
    if not isinstance(matrix, (OpenMaya.MMatrix, OpenMaya.MFloatMatrix)):
        raise TypeError("Invalid argument type given !")
    return [matrix(i, j) for i in range(4) for j in range(4)]


def get_current_time() -> OpenMaya.MTime:
    return OpenMayaAnim.MAnimControl().currentTime()


def start_frame() -> float:
    return cmds.playbackOptions(query=True, min=True)


def end_frame() -> float:
    return cmds.playbackOptions(query=True, max=True)


def go_to_start_frame():
    set_current_time(start_frame())


def time_line_range(start: float = None, end: float = None) -> range:
    start = start_frame() if start is None else start
    end = end_frame() if end is None else end
    return range(int(math.floor(start)), int(math.ceil(end)) + 1)


def set_current_time(time: Union[int, float, OpenMaya.MTime]) -> OpenMaya.MTime:
    if isinstance(time, OpenMaya.MTime):
        time = time.value()

    current_time = get_current_time()
    cmds.currentTime(time)

    return current_time


def get_points(shape: _maya_node, world: bool = True, vertex_ids: list = None) -> OpenMaya.MPointArray:
    if isinstance(shape, (str, OpenMaya.MObject)):
        shape = get_path(shape)

    points = OpenMaya.MPointArray()
    mfn = OpenMaya.MFnMesh(shape)
    space = OpenMaya.MSpace.kWorld if world else OpenMaya.MSpace.kObject

    if not vertex_ids:
        mfn.getPoints(points, space)
    else:
        points.setLength(len(vertex_ids))
        point = OpenMaya.MPoint()
        for i, vertex_id in enumerate(vertex_ids):
            mfn.getPoint(vertex_id, point, space)
            points.set(point, i)

    return points
