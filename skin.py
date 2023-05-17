# coding=ascii
from typing import Union

from maya import cmds, OpenMaya, OpenMayaAnim

from fdda import utils as maya_utils
from fdda.deformer import Deformer
from fdda.logger import log


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

        try:
            influences = OpenMaya.MDagPathArray()
            influences_count = self.mfn.influenceObjects(influences)
            for i in range(influences_count):
                dp_node = influences[i]
                if dp_node.fullPathName() in self.influences_names:
                    continue
                self.influences_ids.append(self.mfn.indexForInfluenceObject(dp_node))
                self.influences_names.append(dp_node.fullPathName())
        except Exception as e:
            log.debug(e)

    def __get_weights(self):
        component = self.__get_shape_component()
        # influences_ids = OpenMaya.MIntArray(self.influence_count())
        # [influences_ids.set(inf_id, i) for i, inf_id in enumerate(self._influences_ids)]
        # ToDo: Understand why with MIntArray.set maya crash
        ids = OpenMaya.MIntArray()
        for inf_id in self.influences_ids:
            ids.append(inf_id)

        self.weights = OpenMaya.MDoubleArray()
        self.mfn.getWeights(maya_utils.get_path(self.shape), component, ids, self.weights)

    def set_weights(self, weights: Union[list, tuple, OpenMaya.MDoubleArray] = None) -> OpenMaya.MDoubleArray:
        """!@Brief Set SkinCluster weight."""
        if not self.object:
            raise Exception("No SkinCluster set !")

        if isinstance(weights, (list, tuple)):
            tmp = OpenMaya.MDoubleArray()
            for w in weights:
                tmp.append(w)
            weights = tmp

        component = self.__get_shape_component()
        if weights is not None:
            self.weights = weights

        influence_ids = OpenMaya.MIntArray()
        for inf_id in self.influences_ids:
            influence_ids.append(inf_id)

        old_weights = OpenMaya.MDoubleArray()
        self.mfn.setWeights(maya_utils.get_path(self.shape), component, influence_ids, self.weights, False, old_weights)

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
    def find(cls, mo_node) -> OpenMaya.MObject:
        return Deformer._find(mo_node, cls.kApiType)
