#ifndef COMMON_H
#define COMMON_H


#include <maya/MTypeId.h>
#include <maya/MPxNode.h>

#include <maya/MFnData.h>
#include <maya/MFnStringData.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MObject.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MQuaternion.h>
#include <maya/MPxDeformerNode.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MEvaluationNode.h>
#include <maya/MItGeometry.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>

#include <vector>
#include <fstream>

#include "nlohmann/json.hpp"
#include <ATen/ATen.h>
#include <nnpack.h>
#include <ATen/cuda/CUDAContext.h>
#include <torch/torch.h>

#include "settings.h"
#include "multiLayerPerceptron.h"


#endif