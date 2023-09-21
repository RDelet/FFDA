# coding=ascii
from typing import Union

from maya import cmds, OpenMaya, OpenMayaAnim

from fdda.core.logger import log
from fdda.core import api_utils
from fdda.core.deformer import Deformer
from fdda.core import constant as cst


class Skin(Deformer):

    kType = 'skinCluster'
    kApiType = OpenMaya.MFn.kSkinClusterFilter

    kSkinningMethod = "skinningMethod"
    kUseComponents = "useComponents"
    kDeformUserNormals = 'deformUserNormals'
    kDqsSupportNonRigid = 'dqsSupportNonRigid'
    kDqsScale = 'dqsScale'
    kNormalizeWeights = 'normalizeWeights'
    kWeightDistribution = 'weightDistribution'
    kMaxInfluences = "maxInfluences"
    kMaintainMaxInfluences = "maintainMaxInfluences"

    # Rotation limits
    kRotateMinX = OpenMaya.MFnTransform.kRotateMinX
    kRotateMaxX = OpenMaya.MFnTransform.kRotateMaxX
    kRotateMinY = OpenMaya.MFnTransform.kRotateMinY
    kRotateMaxY = OpenMaya.MFnTransform.kRotateMaxY
    kRotateMinZ = OpenMaya.MFnTransform.kRotateMinZ
    kRotateMaxZ = OpenMaya.MFnTransform.kRotateMaxZ

    def __init__(self, node: Union[str, OpenMaya.MObject] = None, weights: bool = True):
        super(Skin, self).__init__(node=node)

        self.skinning_method = 0
        self.use_components = False
        self.deform_user_normals = True
        self.dqs_support_non_rigid = False
        self.dqs_scale = [1.0, 1.0, 1.0]
        self.normalize_weights = 1
        self.weight_distribution = 0
        self.max_influences = 8
        self.maintain_max_influences = True
    
        self.influences_ids = list()
        self.influences_names = list()
        self.weights = list()

        if node:
            self.__get(weights=weights)
    
    def influences_count(self) -> int:
        return len(self.influences_ids)

    def __get(self, weights: bool = True):
        self.mfn = OpenMayaAnim.MFnSkinCluster(self.object)
        self.__get_attributes()
        self.__get_influences()
        if weights:
            self.__get_weights()

    def __get_attributes(self):
        name = self.deformer_name

        self.skinning_method = cmds.getAttr(f"{name}.{self.kSkinningMethod}")
        self.use_components = cmds.getAttr(f"{name}.{self.kUseComponents}")
        self.deform_user_normals = cmds.getAttr(f"{name}.{self.kDeformUserNormals}")
        self.dqs_support_non_rigid = cmds.getAttr(f"{name}.{self.kDqsSupportNonRigid}")
        self.dqs_scale = cmds.getAttr(f"{name}.{self.kDqsScale}")
        self.normalize_weights = cmds.getAttr(f"{name}.{self.kNormalizeWeights}")
        self.weight_distribution = cmds.getAttr(f"{name}.{self.kWeightDistribution}")
        self.max_influences = cmds.getAttr(f"{name}.{self.kMaxInfluences}")
        self.maintain_max_influences = cmds.getAttr(f"{name}.{self.kMaintainMaxInfluences}")
    
    def __get_influences(self):
        self.influences_ids = list()
        self.influences_names = list()
        self.influences_ranges = list()
        self.influences_len = None

        try:
            influences = OpenMaya.MDagPathArray()
            influences_count = self.mfn.influenceObjects(influences)
            self.influences_len = OpenMaya.MScriptUtil(influences.length())

            for i in range(influences_count):
                dp_node = influences[i]
                if dp_node.fullPathName() in self.influences_names:
                    continue
                self.influences_ids.append(self.mfn.indexForInfluenceObject(dp_node))
                self.influences_names.append(dp_node.fullPathName())
                self.influences_ranges.append(self.__get_rotation_limits(dp_node))
        except Exception as e:
            log.debug(e)
    
    @classmethod
    def __get_rotation_limits(cls, node):
        mfn = OpenMaya.MFnTransform(node)
        return [[mfn.limitValue(cls.kRotateMinX), mfn.limitValue(cls.kRotateMaxX)],
                [mfn.limitValue(cls.kRotateMinY), mfn.limitValue(cls.kRotateMaxY)],
                [mfn.limitValue(cls.kRotateMinZ), mfn.limitValue(cls.kRotateMaxZ)]]

    def __get_weights(self):
        component = self.__get_shape_component()
        inf_count_ptr = self.influences_len.asUintPtr()
        self.weights = OpenMaya.MDoubleArray()
        shape_path = api_utils.get_path(self.shape)
        self.mfn.getWeights(shape_path, component, self.weights, inf_count_ptr)

    def set_weights(self, weights: Union[list, tuple, OpenMaya.MDoubleArray] = None) -> OpenMaya.MDoubleArray:
        if not self.object:
            raise Exception("No SkinCluster set !")

        component = self.__get_shape_component()

        if isinstance(weights, (list, tuple)):
            tmp = OpenMaya.MDoubleArray()
            for w in weights:
                tmp.append(w)
            weights = tmp
        
        if weights is not None:
            self.weights = weights

        influence_ids = OpenMaya.MIntArray()
        for inf_id in self.influences_ids:
            influence_ids.append(inf_id)

        old_weights = OpenMaya.MDoubleArray()
        shape_path = api_utils.get_path(self.shape)
        self.mfn.setWeights(shape_path, component, influence_ids, self.weights, False, old_weights)

        return old_weights
    
    def __get_shape_component(self) -> OpenMaya.MObject:
        if self.shape.hasFn(OpenMaya.MFn.kMesh):
            mfn = OpenMaya.MFnSingleIndexedComponent()
            component = mfn.create(OpenMaya.MFn.kMeshVertComponent)
            mit = OpenMaya.MItMeshVertex(self.shape)
            while not mit.isDone():
                mfn.addElement(mit.index())
                mit.next()
        else:
            raise RuntimeError(f"Invalid shape type: self._shape.apiTypeStr() !")

        return component

    @classmethod
    def find(cls, node: cst.kdepType) -> "Skin":
        if isinstance(node, str):
            node = api_utils.get_object(node)

        skin_node = Deformer._find(node, cls.kApiType)
        if not node:
            raise RuntimeError(f"No skin cluster found on {api_utils.name(node)} !")

        return cls(skin_node)
