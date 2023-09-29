#ifndef FDDA_NODE_H
#define FDDA_NODE_H


#include "common.h"


class FDDANode : public MPxDeformerNode {

	public:

		FDDANode() {}
		virtual ~FDDANode() {}
		virtual MStatus								deform(MDataBlock& data, MItGeometry& itGeo, const MMatrix& localToWorldMatrix, unsigned int geomIndex);
		virtual MStatus								preEvaluation(const MDGContext& context, const MEvaluationNode& evaluationNode);
		virtual MStatus								setDependentsDirty(const MPlug& plugBeingDirtied, MPlugArray& affectedPlugs);
		static void*								creator() { return new FDDANode(); }
		static MStatus								initialize();

	public:

		// Maya node data
		static MTypeId								kNodeId;
		static MString								kNodeName;
		static MPxNode::Type						kNodeType;

	private:

		static float								getEnveloppe(MDataBlock& data);
		static std::vector<double>					getRotations(MDataBlock& data, unsigned int numModels);
		static void									clear();
		static void									loadModel(MDataBlock& data);
		static void									readModel();
		static TorchModel							deserializeModel(const int& modelID, MDataBlock& data, nlohmann::json& model);
		static void									getPredition();
		static std::vector<MVector>					getDeltas(MItGeometry& itGeo);
		static void									applyDeltas(MDataBlock& data, const std::vector<MVector>& deltas, const float deformerEnveloppe, MItGeometry& itGeo, unsigned int geomIndex);

		// Node attributes
		static MObject								iTrainingData;
		static MObject								iMatrix;

		// data
		static std::string							dataLocation;
		static bool									locationChanged;
		static nlohmann::json						modelData;
		static std::vector<TorchModel>				models;
		static std::vector<std::vector<double>>		means;
		static std::vector<std::vector<double>>		stds;
		static at::Device							device;
		static bool									normalized;
		static bool									globaMode;

		// Json keys
		static std::string							kModels;
		static std::string							kJointMap;
		static std::string							kModel;
		static std::string							kBestModel;
		static std::string							kDevice;
		static std::string							kMean;
		static std::string							kStd;
		static std::string							kNormalized;
		static std::string							kGlobalMode;

		static std::string							kTrainingDataLong;
		static std::string							kTrainingDataShort;
		static std::string							kMatrixLong;
		static std::string							kMatrixShort;

		static nlohmann::json						jsonRoot;

};

#endif