// =================================================================
//	Load Modules
// =================================================================

#include "fddaNode.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin(MObject obj) {

	MStatus	status;
	MFnPlugin	plugin(obj, "Rémi Deletrain -- remi.deletrain@gmail.com", "1.0", "Any");

	status = plugin.registerNode(FDDANode::kNodeName, FDDANode::kNodeId, FDDANode::creator, FDDANode::initialize, FDDANode::kNodeType);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return status;

}

MStatus uninitializePlugin(MObject obj) {

	MStatus     status;
	MFnPlugin	plugin(obj);

	status = plugin.deregisterNode(FDDANode::kNodeId);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return status;

}