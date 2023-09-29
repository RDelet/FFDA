#include "fddaNode.h"


MTypeId								FDDANode::kNodeId(0x174009);
MString								FDDANode::kNodeName("fdda");
MPxNode::Type						FDDANode::kNodeType = MPxNode::kDeformerNode;

MObject								FDDANode::iTrainingData;
MObject								FDDANode::iMatrix;

std::string							FDDANode::dataLocation = "";
bool								FDDANode::locationChanged = false;
nlohmann::json						FDDANode::modelData = std::vector<bool>();
std::vector<TorchModel>				FDDANode::models = std::vector<TorchModel>();
std::vector<std::vector<double>>	FDDANode::means = std::vector<std::vector<double>>();
std::vector<std::vector<double>>	FDDANode::stds = std::vector<std::vector<double>>();
at::Device							FDDANode::device = at::kCPU;
nlohmann::json						FDDANode::jsonRoot = nlohmann::json();
bool								FDDANode::normalized = true;
bool								FDDANode::globaMode = true;

std::string							FDDANode::kModels = "models";
std::string							FDDANode::kJointMap = "joint_map";
std::string							FDDANode::kModel = "model";
std::string							FDDANode::kBestModel = "best_model";
std::string							FDDANode::kDevice = "device";
std::string							FDDANode::kMean = "mean";
std::string							FDDANode::kStd = "std";
std::string							FDDANode::kNormalized = "normalized";

std::string							FDDANode::kGlobalMode = "global_mode";
std::string							FDDANode::kTrainingDataLong = "trainingData";
std::string							FDDANode::kTrainingDataShort = "ta";
std::string							FDDANode::kMatrixLong = "matrix";
std::string							FDDANode::kMatrixShort = "mat";


MStatus FDDANode::initialize() {

	MStatus status;

	MFnStringData stringDataFn;
	MObject stringData = stringDataFn.create(&status);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	MFnTypedAttribute trainingDataAttr;
	iTrainingData = trainingDataAttr.create("trainingData", "ta", MFnData::kString, stringData, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	CHECK_MSTATUS_AND_RETURN_IT(trainingDataAttr.setKeyable(false));
	CHECK_MSTATUS_AND_RETURN_IT(trainingDataAttr.setStorable(true));
	CHECK_MSTATUS_AND_RETURN_IT(FDDANode::addAttribute(iTrainingData));
	attributeAffects(iTrainingData, outputGeom);

	MFnMatrixAttribute matrixAttr;
	iMatrix = matrixAttr.create("matrix", "matrix", MFnMatrixAttribute::kDouble, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	CHECK_MSTATUS_AND_RETURN_IT(matrixAttr.setKeyable(true));
	CHECK_MSTATUS_AND_RETURN_IT(matrixAttr.setStorable(true));
	CHECK_MSTATUS_AND_RETURN_IT(matrixAttr.setArray(true));
	CHECK_MSTATUS_AND_RETURN_IT(FDDANode::addAttribute(iMatrix));
	attributeAffects(iMatrix, outputGeom);

	return MS::kSuccess;

}


MStatus FDDANode::preEvaluation(const MDGContext& context, const MEvaluationNode& evaluationNode) {

	MStatus status;

	if (evaluationNode.dirtyPlugExists(iTrainingData)) {
		locationChanged = true;
	}

	return status.kSuccess;

}


MStatus FDDANode::setDependentsDirty(const MPlug& plugBeingDirtied, MPlugArray& affectedPlugs) {

	MStatus status;

	if (plugBeingDirtied == iTrainingData) {
		locationChanged = true;
	}

	return status.kSuccess;

}


float FDDANode::getEnveloppe(MDataBlock& data) {
	return data.inputValue(MPxDeformerNode::envelope).asFloat();
}


std::vector<double> FDDANode::getRotations(MDataBlock& data, unsigned int numModels) {

	std::vector<double> rotations;

	MArrayDataHandle matricesHandle = data.inputArrayValue(iMatrix);

	unsigned int matrixCount = matricesHandle.elementCount();
	if (matrixCount > numModels) {
		MGlobal::displayWarning("More input joints than models !");
		return rotations;
	}

	for (unsigned int i = 0; i < matrixCount; i++) {
		matricesHandle.jumpToElement(i);
		MDataHandle matrixHandle = matricesHandle.inputValue();
		// Conversion homogenous transformation matrix (4x4) to quaternion and translation vector
		MTransformationMatrix transformation(matrixHandle.asMatrix());
		MQuaternion quaternion = transformation.rotation();
		rotations.push_back(quaternion.x);
		rotations.push_back(quaternion.y);
		rotations.push_back(quaternion.z);
		rotations.push_back(quaternion.w);
	}

	return rotations;

}


void FDDANode::clear() {
	dataLocation = "";
	models.clear();
	means.clear();
	stds.clear();
}


void FDDANode::loadModel(MDataBlock& data) {

	dataLocation = data.inputValue(iTrainingData).asString().asChar();
	std::string msg = "Loading models from: " + dataLocation + ".";
	MGlobal::displayInfo(msg.c_str());

	clear();
	readModel();
	if (!jsonRoot.contains(kModels)) {
		MGlobal::displayError("No models defined in data !");
	}

	modelData = jsonRoot[kModels];
	if (!modelData.is_array()) {
		MGlobal::displayError("Invalid model data !");
	}

	if (jsonRoot.contains(kNormalized)) {
		normalized = jsonRoot[kNormalized];
	}

	if (jsonRoot.contains(kGlobalMode)) {
		normalized = jsonRoot[kGlobalMode];
	}

	// Vérifiez si un GPU est disponible
	if (at::cuda::device_count() > 0) {
		device = at::kCUDA;
	}

	int i = 0;
	for (auto& element : modelData) {

		std::vector<double> mean;
		std::vector<double> std;
		TorchModel model;

		if (!element.empty()) {
			mean = element[kMean].template get<std::vector<double>>();
			std = element[kStd].template get<std::vector<double>>();
			model = deserializeModel(i, data, element);
		}

		means.push_back(mean);
		stds.push_back(std);
		models.push_back(model);

		i++;
	}

}


void FDDANode::readModel() {

	if (!locationChanged) {
		return;
	}

	std::ifstream file(dataLocation);
	if (!file.good()){
		return;
	}
	
	jsonRoot = nlohmann::json::parse(file);
	if (jsonRoot.empty() || jsonRoot.is_null()) {
		std::string msg = "Impossible to read file" + dataLocation + " !";
		MGlobal::displayWarning(msg.c_str());
	}

	locationChanged = false;

}


TorchModel FDDANode::deserializeModel(const int& modelID, MDataBlock& data, nlohmann::json& model) {

	std::vector<int> vertices;
	if (globaMode) {
		std::vector<std::vector<int>> jointMap = model[kJointMap].template get<std::vector<std::vector<int>>>();
		for (size_t i = 0; i < jointMap.size(); i++) {
			for (size_t j = 0; j < jointMap[i].size(); j++) {
				vertices.push_back(jointMap[i][j]);
			}
		}
	}
	else {
		vertices = model[kJointMap][modelID].template get<std::vector<int>>();
	}

	auto checkpoint = torch::jit::load(model[kBestModel]);
	MultiLayerPerceptron model = MultiLayerPerceptron(checkpoint["settings"], checkpoint["input_shape"], checkpoint["output_shape"]);
	model.to(device);
	model.load_state_dict(checkpoint["model_state_dict"]);

	return TorchModel{ model , vertices};

}


void FDDANode::getPredition() {}


std::vector<MVector> FDDANode::getDeltas(MItGeometry& itGeo) {

	std::vector<MVector> deltas;

	return deltas;

}


void FDDANode::applyDeltas(MDataBlock& data, const std::vector<MVector>& deltas, const float deformerEnveloppe, MItGeometry& itGeo, unsigned int geomIndex) {

	MPointArray points;
	while (!itGeo.isDone()) {
		unsigned int index = itGeo.index();
		MPoint pointPosition = itGeo.position();
		float vtxWeight = 1.0; // weightValue(data, geomIndex, index);
		
		pointPosition += deltas[index] * deformerEnveloppe * vtxWeight;
		points.set(pointPosition, index);
		itGeo.next();
	}

	itGeo.setAllPositions(points);

}


MStatus FDDANode::deform(MDataBlock& data, MItGeometry& itGeo, const MMatrix& localToWorldMatrix, unsigned int geomIndex) {

	MStatus status;

	if (locationChanged) {
		loadModel(data);
	}

	unsigned int numModels = unsigned int(models.size());
	if (numModels == 0) {
		MGlobal::displayInfo("No model found !");
		return MS::kSuccess;
	}

	float deformerEnveloppe = getEnveloppe(data);
	std::vector<double> rotations = getRotations(data, numModels);
	std::vector<MVector> deltas = getDeltas(itGeo);
	applyDeltas(data, deltas, deformerEnveloppe, itGeo, geomIndex);

	return MS::kSuccess;

}
