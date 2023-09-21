//Maya ASCII 2022 scene
//Name: CylinderTest.ma
//Last modified: Thu, Sep 21, 2023 06:39:35 PM
//Codeset: 1252
requires maya "2022";
requires "stereoCamera" "10.0";
requires -nodeType "aiOptions" -nodeType "aiAOVDriver" -nodeType "aiAOVFilter" "mtoa" "5.0.0.4";
currentUnit -linear centimeter -angle degree -time ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2022";
fileInfo "version" "2022";
fileInfo "cutIdentifier" "202205171752-c25c06f306";
fileInfo "osv" "Windows 10 Enterprise v2009 (Build: 19044)";
fileInfo "UUID" "108679FB-4479-9E52-6B9E-7BBD27B4B10C";
createNode transform -shared -name "persp";
	rename -uuid "D913A6CE-415F-9BE2-9565-D5B1208FC596";
	setAttr ".visibility" no;
	setAttr ".translate" -type "double3" 5.8736211823526139 6.1148700972292147 9.9099700276068461 ;
	setAttr ".rotate" -type "double3" -17.738352729616626 -338.99999999998062 8.5170880600972609e-16 ;
createNode camera -shared -name "perspShape" -parent "persp";
	rename -uuid "3AC59194-474F-39B9-D278-1EB3EB112607";
	setAttr -keyable off ".visibility" no;
	setAttr ".focalLength" 34.999999999999993;
	setAttr ".centerOfInterest" 12.32598468258487;
	setAttr ".imageName" -type "string" "persp";
	setAttr ".depthName" -type "string" "persp_depth";
	setAttr ".maskName" -type "string" "persp_mask";
	setAttr ".homeCommand" -type "string" "viewSet -p %camera";
createNode transform -shared -name "top";
	rename -uuid "F508EE17-4C1F-E75B-0F94-F0A144CCA2E7";
	setAttr ".visibility" no;
	setAttr ".translate" -type "double3" 0 1000.1 0 ;
	setAttr ".rotate" -type "double3" -90 0 0 ;
createNode camera -shared -name "topShape" -parent "top";
	rename -uuid "3B13E480-4673-B1FF-44A6-D68CF4F8548B";
	setAttr -keyable off ".visibility" no;
	setAttr ".renderable" no;
	setAttr ".centerOfInterest" 1000.1;
	setAttr ".orthographicWidth" 30;
	setAttr ".imageName" -type "string" "top";
	setAttr ".depthName" -type "string" "top_depth";
	setAttr ".maskName" -type "string" "top_mask";
	setAttr ".homeCommand" -type "string" "viewSet -t %camera";
	setAttr ".orthographic" yes;
	setAttr ".aiTranslator" -type "string" "orthographic";
createNode transform -shared -name "front";
	rename -uuid "DFFBF7AC-4972-F653-6E1E-3E90F10B959D";
	setAttr ".visibility" no;
	setAttr ".translate" -type "double3" 0 0 1000.1 ;
createNode camera -shared -name "frontShape" -parent "front";
	rename -uuid "28FD74E1-4DF0-1D7B-C77A-C68438FC6760";
	setAttr -keyable off ".visibility" no;
	setAttr ".renderable" no;
	setAttr ".centerOfInterest" 1000.1;
	setAttr ".orthographicWidth" 30;
	setAttr ".imageName" -type "string" "front";
	setAttr ".depthName" -type "string" "front_depth";
	setAttr ".maskName" -type "string" "front_mask";
	setAttr ".homeCommand" -type "string" "viewSet -f %camera";
	setAttr ".orthographic" yes;
	setAttr ".aiTranslator" -type "string" "orthographic";
createNode transform -shared -name "side";
	rename -uuid "C7F1F531-40C9-52F2-462D-B786E622859F";
	setAttr ".visibility" no;
	setAttr ".translate" -type "double3" 1000.1 2.1921595882814922 -1.0272737719846559 ;
	setAttr ".rotate" -type "double3" 0 90 0 ;
createNode camera -shared -name "sideShape" -parent "side";
	rename -uuid "C24D6944-44CC-7174-6147-CDB78ECDC560";
	setAttr -keyable off ".visibility" no;
	setAttr ".renderable" no;
	setAttr ".centerOfInterest" 1000.1;
	setAttr ".orthographicWidth" 14.43979809899435;
	setAttr ".imageName" -type "string" "side";
	setAttr ".depthName" -type "string" "side_depth";
	setAttr ".maskName" -type "string" "side_mask";
	setAttr ".homeCommand" -type "string" "viewSet -s %camera";
	setAttr ".orthographic" yes;
	setAttr ".aiTranslator" -type "string" "orthographic";
createNode transform -name "ROOT";
	rename -uuid "EEFD0F21-47C4-DC11-41EE-F5A5E1C2AA60";
createNode transform -name "MESHES" -parent "ROOT";
	rename -uuid "9DEC2C4E-4182-D975-8663-60A9BC65FAC5";
createNode transform -name "Cylinder_SRC" -parent "MESHES";
	rename -uuid "9ED5801E-4814-AF82-14A3-DB976376FCF0";
	setAttr ".translate" -type "double3" 0 3 0 ;
	setAttr -lock on ".translateX";
	setAttr -lock on ".translateY";
	setAttr -lock on ".translateZ";
	setAttr -lock on ".rotateX";
	setAttr -lock on ".rotateY";
	setAttr -lock on ".rotateZ";
	setAttr -lock on ".scaleX";
	setAttr -lock on ".scaleY";
	setAttr -lock on ".scaleZ";
createNode mesh -name "Cylinder_SRCShape" -parent "Cylinder_SRC";
	rename -uuid "E532591F-4989-9649-E32D-9695C864DE4C";
	setAttr -keyable off ".visibility";
	setAttr ".visibleInReflections" yes;
	setAttr ".visibleInRefractions" yes;
	setAttr ".uvSet[0].uvSetName" -type "string" "map1";
	setAttr ".currentUVSet" -type "string" "map1";
	setAttr ".displayColorChannel" -type "string" "Ambient+Diffuse";
	setAttr ".collisionOffsetVelocityMultiplier[0]"  0 1 1;
	setAttr ".collisionDepthVelocityMultiplier[0]"  0 1 1;
	setAttr ".vertexColorSource" 2;
createNode mesh -name "Cylinder_SRCShapeOrig" -parent "Cylinder_SRC";
	rename -uuid "89699AC0-4DE7-96DB-838D-A69B883468ED";
	setAttr -keyable off ".visibility";
	setAttr ".intermediateObject" yes;
	setAttr ".visibleInReflections" yes;
	setAttr ".visibleInRefractions" yes;
	setAttr ".uvSet[0].uvSetName" -type "string" "map1";
	setAttr ".currentUVSet" -type "string" "map1";
	setAttr ".displayColorChannel" -type "string" "Ambient+Diffuse";
	setAttr ".collisionOffsetVelocityMultiplier[0]"  0 1 1;
	setAttr ".collisionDepthVelocityMultiplier[0]"  0 1 1;
createNode transform -name "JOINTS" -parent "ROOT";
	rename -uuid "C6EEC47F-40B8-433F-569D-CE8B9BA9CC57";
createNode joint -name "joint1" -parent "JOINTS";
	rename -uuid "63749E5E-4179-CC53-0A9B-EB9A85FC4407";
	addAttr -cachedInternally true -shortName "liw" -longName "lockInfluenceWeights" 
		-minValue 0 -maxValue 1 -attributeType "bool";
	setAttr ".useObjectColor" 1;
	setAttr ".minRotLimit" -type "double3" -360 -360 -360 ;
	setAttr ".maxRotLimit" -type "double3" 360 360 360 ;
	setAttr ".jointOrient" -type "double3" 0 0 90 ;
	setAttr ".bindPose" -type "matrix" 0 1 0 0 -1 0 0 0 0 0 1 0 0 0 0 1;
	setAttr ".radius" 0.55172413793103448;
createNode joint -name "joint2" -parent "joint1";
	rename -uuid "3F6AD6A4-4358-569E-D4AA-E8B8E0B37BE0";
	addAttr -cachedInternally true -shortName "liw" -longName "lockInfluenceWeights" 
		-minValue 0 -maxValue 1 -attributeType "bool";
	setAttr ".useObjectColor" 1;
	setAttr ".objectColor" 1;
	setAttr ".translate" -type "double3" 2 0 0 ;
	setAttr ".minRotLimit" -type "double3" -45 -90 -90 ;
	setAttr ".maxRotLimit" -type "double3" 45 90 90 ;
	setAttr ".minRotXLimitEnable" yes;
	setAttr ".minRotYLimitEnable" yes;
	setAttr ".minRotZLimitEnable" yes;
	setAttr ".maxRotXLimitEnable" yes;
	setAttr ".maxRotYLimitEnable" yes;
	setAttr ".maxRotZLimitEnable" yes;
	setAttr ".bindPose" -type "matrix" 0 1 0 0 -1 0 0 0 0 0 1 0 0 2 0 1;
	setAttr ".radius" 0.55172413793103448;
createNode joint -name "joint3" -parent "joint2";
	rename -uuid "696E619B-4FA2-CFF3-BC2F-9FAFAE884808";
	addAttr -cachedInternally true -shortName "liw" -longName "lockInfluenceWeights" 
		-minValue 0 -maxValue 1 -attributeType "bool";
	setAttr ".useObjectColor" 1;
	setAttr ".objectColor" 2;
	setAttr ".translate" -type "double3" 2 0 0 ;
	setAttr ".minRotLimit" -type "double3" -45 -90 -90 ;
	setAttr ".maxRotLimit" -type "double3" 45 90 90 ;
	setAttr ".minRotXLimitEnable" yes;
	setAttr ".minRotYLimitEnable" yes;
	setAttr ".minRotZLimitEnable" yes;
	setAttr ".maxRotXLimitEnable" yes;
	setAttr ".maxRotYLimitEnable" yes;
	setAttr ".maxRotZLimitEnable" yes;
	setAttr ".bindPose" -type "matrix" 0 1 0 0 -1 0 0 0 0 0 1 0 0 4 0 1;
	setAttr ".radius" 0.55172413793103448;
createNode joint -name "joint4" -parent "joint3";
	rename -uuid "F8823AC0-42FE-E202-CCB0-FB95CB863B58";
	setAttr ".useObjectColor" 1;
	setAttr ".objectColor" 3;
	setAttr ".translate" -type "double3" 2 0 0 ;
	setAttr ".minRotLimit" -type "double3" -360 -360 -360 ;
	setAttr ".maxRotLimit" -type "double3" 360 360 360 ;
	setAttr ".jointOrient" -type "double3" 0 0 -90 ;
	setAttr ".radius" 0.55172413793103448;
createNode transform -name "FDDA";
	rename -uuid "A901CE63-4FFA-1E3D-D00D-6FBCF500A13D";
createNode transform -name "Cylinder_DST" -parent "FDDA";
	rename -uuid "DE9B75DF-4208-D288-6915-D9AE53D97979";
	setAttr ".translate" -type "double3" 0 3 0 ;
	setAttr -lock on ".translateX";
	setAttr -lock on ".translateY";
	setAttr -lock on ".translateZ";
	setAttr -lock on ".rotateX";
	setAttr -lock on ".rotateY";
	setAttr -lock on ".rotateZ";
	setAttr -lock on ".scaleX";
	setAttr -lock on ".scaleY";
	setAttr -lock on ".scaleZ";
createNode mesh -name "Cylinder_DSTShape" -parent "Cylinder_DST";
	rename -uuid "E43F6236-43AD-AF50-3320-9A8131BDEB48";
	setAttr -keyable off ".visibility";
	setAttr ".visibleInReflections" yes;
	setAttr ".visibleInRefractions" yes;
	setAttr ".uvSet[0].uvSetName" -type "string" "map1";
	setAttr ".currentUVSet" -type "string" "map1";
	setAttr ".displayColorChannel" -type "string" "Ambient+Diffuse";
	setAttr ".collisionOffsetVelocityMultiplier[0]"  0 1 1;
	setAttr ".collisionDepthVelocityMultiplier[0]"  0 1 1;
	setAttr ".vertexColorSource" 2;
createNode mesh -name "Cylinder_DSTShapeOrig" -parent "Cylinder_DST";
	rename -uuid "3F5BAE62-4C08-4DC1-8814-96B3B17D1779";
	setAttr -keyable off ".visibility";
	setAttr ".intermediateObject" yes;
	setAttr ".visibleInReflections" yes;
	setAttr ".visibleInRefractions" yes;
	setAttr -size 10 ".componentTags";
	setAttr ".componentTags[0].componentTagName" -type "string" "bottom";
	setAttr ".componentTags[0].componentTagContents" -type "componentList" 1 "f[120:139]";
	setAttr ".componentTags[1].componentTagName" -type "string" "bottomRing";
	setAttr ".componentTags[1].componentTagContents" -type "componentList" 1 "e[0:19]";
	setAttr ".componentTags[2].componentTagName" -type "string" "cylBottomCap";
	setAttr ".componentTags[2].componentTagContents" -type "componentList" 2 "vtx[0:19]" "vtx[140]";
	setAttr ".componentTags[3].componentTagName" -type "string" "cylBottomRing";
	setAttr ".componentTags[3].componentTagContents" -type "componentList" 1 "vtx[0:19]";
	setAttr ".componentTags[4].componentTagName" -type "string" "cylSides";
	setAttr ".componentTags[4].componentTagContents" -type "componentList" 1 "vtx[0:139]";
	setAttr ".componentTags[5].componentTagName" -type "string" "cylTopCap";
	setAttr ".componentTags[5].componentTagContents" -type "componentList" 2 "vtx[120:139]" "vtx[141]";
	setAttr ".componentTags[6].componentTagName" -type "string" "cylTopRing";
	setAttr ".componentTags[6].componentTagContents" -type "componentList" 1 "vtx[120:139]";
	setAttr ".componentTags[7].componentTagName" -type "string" "sides";
	setAttr ".componentTags[7].componentTagContents" -type "componentList" 1 "f[0:119]";
	setAttr ".componentTags[8].componentTagName" -type "string" "top";
	setAttr ".componentTags[8].componentTagContents" -type "componentList" 1 "f[140:159]";
	setAttr ".componentTags[9].componentTagName" -type "string" "topRing";
	setAttr ".componentTags[9].componentTagContents" -type "componentList" 1 "e[120:139]";
	setAttr ".uvSet[0].uvSetName" -type "string" "map1";
	setAttr -size 189 ".uvSet[0].uvSetPoints[0:188]" -type "float2" 0.64860266
		 0.10796607 0.62640899 0.064408496 0.59184152 0.029841021 0.54828393 0.0076473355
		 0.5 -7.4505806e-08 0.45171607 0.0076473504 0.40815851 0.029841051 0.37359107 0.064408526
		 0.3513974 0.1079661 0.34374997 0.15625 0.3513974 0.2045339 0.37359107 0.24809146
		 0.40815854 0.28265893 0.4517161 0.3048526 0.5 0.3125 0.54828387 0.3048526 0.59184146
		 0.28265893 0.62640893 0.24809146 0.6486026 0.2045339 0.65625 0.15625 0.375 0.3125
		 0.38749999 0.3125 0.39999998 0.3125 0.41249996 0.3125 0.42499995 0.3125 0.43749994
		 0.3125 0.44999993 0.3125 0.46249992 0.3125 0.4749999 0.3125 0.48749989 0.3125 0.49999988
		 0.3125 0.51249987 0.3125 0.52499986 0.3125 0.53749985 0.3125 0.54999983 0.3125 0.56249982
		 0.3125 0.57499981 0.3125 0.5874998 0.3125 0.59999979 0.3125 0.61249977 0.3125 0.62499976
		 0.3125 0.375 0.375 0.38749999 0.375 0.39999998 0.375 0.41249996 0.375 0.42499995
		 0.375 0.43749994 0.375 0.44999993 0.375 0.46249992 0.375 0.4749999 0.375 0.48749989
		 0.375 0.49999988 0.375 0.51249987 0.375 0.52499986 0.375 0.53749985 0.375 0.54999983
		 0.375 0.56249982 0.375 0.57499981 0.375 0.5874998 0.375 0.59999979 0.375 0.61249977
		 0.375 0.62499976 0.375 0.375 0.4375 0.38749999 0.4375 0.39999998 0.4375 0.41249996
		 0.4375 0.42499995 0.4375 0.43749994 0.4375 0.44999993 0.4375 0.46249992 0.4375 0.4749999
		 0.4375 0.48749989 0.4375 0.49999988 0.4375 0.51249987 0.4375 0.52499986 0.4375 0.53749985
		 0.4375 0.54999983 0.4375 0.56249982 0.4375 0.57499981 0.4375 0.5874998 0.4375 0.59999979
		 0.4375 0.61249977 0.4375 0.62499976 0.4375 0.375 0.5 0.38749999 0.5 0.39999998 0.5
		 0.41249996 0.5 0.42499995 0.5 0.43749994 0.5 0.44999993 0.5 0.46249992 0.5 0.4749999
		 0.5 0.48749989 0.5 0.49999988 0.5 0.51249987 0.5 0.52499986 0.5 0.53749985 0.5 0.54999983
		 0.5 0.56249982 0.5 0.57499981 0.5 0.5874998 0.5 0.59999979 0.5 0.61249977 0.5 0.62499976
		 0.5 0.375 0.5625 0.38749999 0.5625 0.39999998 0.5625 0.41249996 0.5625 0.42499995
		 0.5625 0.43749994 0.5625 0.44999993 0.5625 0.46249992 0.5625 0.4749999 0.5625 0.48749989
		 0.5625 0.49999988 0.5625 0.51249987 0.5625 0.52499986 0.5625 0.53749985 0.5625 0.54999983
		 0.5625 0.56249982 0.5625 0.57499981 0.5625 0.5874998 0.5625 0.59999979 0.5625 0.61249977
		 0.5625 0.62499976 0.5625 0.375 0.625 0.38749999 0.625 0.39999998 0.625 0.41249996
		 0.625 0.42499995 0.625 0.43749994 0.625 0.44999993 0.625 0.46249992 0.625 0.4749999
		 0.625 0.48749989 0.625 0.49999988 0.625 0.51249987 0.625 0.52499986 0.625 0.53749985
		 0.625 0.54999983 0.625 0.56249982 0.625 0.57499981 0.625 0.5874998 0.625 0.59999979
		 0.625 0.61249977 0.625 0.62499976 0.625 0.375 0.6875 0.38749999 0.6875 0.39999998
		 0.6875 0.41249996 0.6875 0.42499995 0.6875 0.43749994 0.6875 0.44999993 0.6875 0.46249992
		 0.6875 0.4749999 0.6875 0.48749989 0.6875 0.49999988 0.6875 0.51249987 0.6875 0.52499986
		 0.6875 0.53749985 0.6875 0.54999983 0.6875 0.56249982 0.6875 0.57499981 0.6875 0.5874998
		 0.6875 0.59999979 0.6875 0.61249977 0.6875 0.62499976 0.6875 0.64860266 0.79546607
		 0.62640899 0.75190848 0.59184152 0.71734101 0.54828393 0.69514734 0.5 0.68749994
		 0.45171607 0.69514734 0.40815851 0.71734107 0.37359107 0.75190854 0.3513974 0.79546607
		 0.34374997 0.84375 0.3513974 0.89203393 0.37359107 0.93559146 0.40815854 0.97015893
		 0.4517161 0.9923526 0.5 1 0.54828387 0.9923526 0.59184146 0.97015893 0.62640893 0.93559146
		 0.6486026 0.89203393 0.65625 0.84375 0.5 0.15625 0.5 0.84375;
	setAttr ".currentUVSet" -type "string" "map1";
	setAttr ".displayColorChannel" -type "string" "Ambient+Diffuse";
	setAttr ".collisionOffsetVelocityMultiplier[0]"  0 1 1;
	setAttr ".collisionDepthVelocityMultiplier[0]"  0 1 1;
	setAttr -size 142 ".vrts[0:141]"  0.95105714 -3 -0.30901718 0.80901754 -3 -0.5877856
		 0.5877856 -3 -0.80901748 0.30901715 -3 -0.95105702 8.5404744e-18 -3 -1.000000476837
		 -0.30901715 -3 -0.95105696 -0.58778548 -3 -0.8090173 -0.80901724 -3 -0.58778542 -0.95105678 -3 -0.30901706
		 -1.000000238419 -3 3.1900953e-15 -0.95105678 -3 0.30901706 -0.80901718 -3 0.58778536
		 -0.58778536 -3 0.80901712 -0.30901706 -3 0.95105666 -2.9802322e-08 -3 1.000000119209
		 0.30901697 -3 0.9510566 0.58778524 -3 0.80901706 0.809017 -3 0.5877853 0.95105654 -3 0.309017
		 1 -3 -9.6291383e-15 0.95105714 -2 -0.30901718 0.80901754 -2 -0.5877856 0.5877856 -2 -0.80901748
		 0.30901715 -2 -0.95105702 1.0270879e-10 -2 -1.000000476837 -0.30901715 -2 -0.95105696
		 -0.58778548 -2 -0.8090173 -0.80901724 -2 -0.58778542 -0.95105678 -2 -0.30901706 -1.000000238419 -2 1.8552433e-10
		 -0.95105678 -2 0.30901706 -0.80901718 -2 0.58778536 -0.58778536 -2 0.80901712 -0.30901706 -2 0.95105666
		 -2.9647101e-08 -2 1.000000119209 0.30901697 -2 0.9510566 0.58778524 -2 0.80901706
		 0.809017 -2 0.5877853 0.95105654 -2 0.309017 1 -2 -1.6855843e-10 0.95105714 -1 -0.30901718
		 0.80901754 -1 -0.5877856 0.5877856 -1 -0.80901748 0.30901715 -1 -0.95105702 6.8639144e-12 -1 -1.000000476837
		 -0.30901715 -1 -0.95105696 -0.58778548 -1 -0.8090173 -0.80901724 -1 -0.58778542 -0.95105678 -1 -0.30901706
		 -1.000000238419 -1 3.4963872e-11 -0.95105678 -1 0.30901706 -0.80901718 -1 0.58778536
		 -0.58778536 -1 0.80901712 -0.30901706 -1 0.95105666 -2.9816263e-08 -1 1.000000119209
		 0.30901697 -1 0.9510566 0.58778524 -1 0.80901706 0.809017 -1 0.5877853 0.95105654 -1 0.309017
		 1 -1 2.1249865e-11 0.95105714 2.103841e-16 -0.30901718 0.80901754 1.326843e-16 -0.5877856
		 0.5877856 5.4927874e-16 -0.80901748 0.30901715 2.7609796e-16 -0.95105702 -9.899372e-17 1.5672987e-16 -1.000000476837
		 -0.30901715 -1.6623416e-16 -0.95105696 -0.58778548 -1.9542388e-16 -0.8090173 -0.80901724 -8.2047608e-16 -0.58778542
		 -0.95105678 8.1273817e-17 -0.30901706 -1.000000238419 0 0 -0.95105678 -1.3079905e-16 0.30901706
		 -0.80901718 8.1273817e-17 0.58778536 -0.58778536 -2.8848314e-17 0.80901712 -0.30901706 7.4291976e-17 0.95105666
		 -2.9802322e-08 4.4339226e-16 1.000000119209 0.30901697 2.5782277e-16 0.9510566 0.58778524 8.1273817e-17 0.80901706
		 0.809017 2.1496422e-16 0.5877853 0.95105654 6.5707591e-16 0.309017 1 -3.1793302e-16 5.5640123e-16
		 0.95105714 1 -0.30901718 0.80901754 1 -0.5877856 0.5877856 1 -0.80901748 0.30901715 1 -0.95105702
		 -8.0129116e-13 1 -1.000000476837 -0.30901715 1 -0.95105696 -0.58778548 1 -0.8090173
		 -0.80901724 1 -0.58778542 -0.95105678 1 -0.30901706 -1.000000238419 1 -2.3622816e-11
		 -0.95105678 1 0.30901706 -0.80901718 1 0.58778536 -0.58778536 1 0.80901712 -0.30901706 1 0.95105666
		 -2.9799752e-08 1 1.000000119209 0.30901697 1 0.9510566 0.58778524 1 0.80901706 0.809017 1 0.5877853
		 0.95105654 1 0.309017 1 1 1.4318295e-11 0.95105714 2 -0.30901718 0.80901754 2 -0.5877856
		 0.5877856 2 -0.80901748 0.30901715 2 -0.95105702 -2.3700519e-10 2 -1.000000476837
		 -0.30901715 2 -0.95105696 -0.58778548 2 -0.8090173 -0.80901724 2 -0.58778542 -0.95105678 2 -0.30901706
		 -1.000000238419 2 1.1550454e-12 -0.95105678 2 0.30901706 -0.80901718 2 0.58778536
		 -0.58778536 2 0.80901712 -0.30901706 2 0.95105666 -2.9388584e-08 2 1.000000119209
		 0.30901697 2 0.9510566 0.58778524 2 0.80901706 0.809017 2 0.5877853 0.95105654 2 0.309017
		 1 2 3.3530032e-10 0.95105714 3 -0.30901718 0.80901754 3 -0.5877856 0.5877856 3 -0.80901748
		 0.30901715 3 -0.95105702 1.9893887e-10 3 -1.000000476837 -0.30901715 3 -0.95105696
		 -0.58778548 3 -0.8090173 -0.80901724 3 -0.58778542 -0.95105678 3 -0.30901706 -1.000000238419 3 -1.3943724e-10
		 -0.95105678 3 0.30901706 -0.80901718 3 0.58778536 -0.58778536 3 0.80901712 -0.30901706 3 0.95105666
		 -2.9966106e-08 3 1.000000119209 0.30901697 3 0.9510566 0.58778524 3 0.80901706 0.809017 3 0.5877853
		 0.95105654 3 0.309017 1 3 -2.4098637e-10 1.6455601e-15 -3 -3.4082022e-16 1.0119225e-15 3 8.2678113e-16;
	setAttr -size 300 ".edge";
	setAttr ".edge[0:165]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 6 0 6 7 0 7 8 0 8 9 0
		 9 10 0 10 11 0 11 12 0 12 13 0 13 14 0 14 15 0 15 16 0 16 17 0 17 18 0 18 19 0 19 0 0
		 20 21 1 21 22 1 22 23 1 23 24 1 24 25 1 25 26 1 26 27 1 27 28 1 28 29 1 29 30 1 30 31 1
		 31 32 1 32 33 1 33 34 1 34 35 1 35 36 1 36 37 1 37 38 1 38 39 1 39 20 1 40 41 1 41 42 1
		 42 43 1 43 44 1 44 45 1 45 46 1 46 47 1 47 48 1 48 49 1 49 50 1 50 51 1 51 52 1 52 53 1
		 53 54 1 54 55 1 55 56 1 56 57 1 57 58 1 58 59 1 59 40 1 60 61 1 61 62 1 62 63 1 63 64 1
		 64 65 1 65 66 1 66 67 1 67 68 1 68 69 1 69 70 1 70 71 1 71 72 1 72 73 1 73 74 1 74 75 1
		 75 76 1 76 77 1 77 78 1 78 79 1 79 60 1 80 81 1 81 82 1 82 83 1 83 84 1 84 85 1 85 86 1
		 86 87 1 87 88 1 88 89 1 89 90 1 90 91 1 91 92 1 92 93 1 93 94 1 94 95 1 95 96 1 96 97 1
		 97 98 1 98 99 1 99 80 1 100 101 1 101 102 1 102 103 1 103 104 1 104 105 1 105 106 1
		 106 107 1 107 108 1 108 109 1 109 110 1 110 111 1 111 112 1 112 113 1 113 114 1 114 115 1
		 115 116 1 116 117 1 117 118 1 118 119 1 119 100 1 120 121 0 121 122 0 122 123 0 123 124 0
		 124 125 0 125 126 0 126 127 0 127 128 0 128 129 0 129 130 0 130 131 0 131 132 0 132 133 0
		 133 134 0 134 135 0 135 136 0 136 137 0 137 138 0 138 139 0 139 120 0 0 20 1 1 21 1
		 2 22 1 3 23 1 4 24 1 5 25 1 6 26 1 7 27 1 8 28 1 9 29 1 10 30 1 11 31 1 12 32 1 13 33 1
		 14 34 1 15 35 1 16 36 1 17 37 1 18 38 1 19 39 1 20 40 1 21 41 1 22 42 1 23 43 1 24 44 1
		 25 45 1;
	setAttr ".edge[166:299]" 26 46 1 27 47 1 28 48 1 29 49 1 30 50 1 31 51 1 32 52 1
		 33 53 1 34 54 1 35 55 1 36 56 1 37 57 1 38 58 1 39 59 1 40 60 1 41 61 1 42 62 1 43 63 1
		 44 64 1 45 65 1 46 66 1 47 67 1 48 68 1 49 69 1 50 70 1 51 71 1 52 72 1 53 73 1 54 74 1
		 55 75 1 56 76 1 57 77 1 58 78 1 59 79 1 60 80 1 61 81 1 62 82 1 63 83 1 64 84 1 65 85 1
		 66 86 1 67 87 1 68 88 1 69 89 1 70 90 1 71 91 1 72 92 1 73 93 1 74 94 1 75 95 1 76 96 1
		 77 97 1 78 98 1 79 99 1 80 100 1 81 101 1 82 102 1 83 103 1 84 104 1 85 105 1 86 106 1
		 87 107 1 88 108 1 89 109 1 90 110 1 91 111 1 92 112 1 93 113 1 94 114 1 95 115 1
		 96 116 1 97 117 1 98 118 1 99 119 1 100 120 1 101 121 1 102 122 1 103 123 1 104 124 1
		 105 125 1 106 126 1 107 127 1 108 128 1 109 129 1 110 130 1 111 131 1 112 132 1 113 133 1
		 114 134 1 115 135 1 116 136 1 117 137 1 118 138 1 119 139 1 140 0 1 140 1 1 140 2 1
		 140 3 1 140 4 1 140 5 1 140 6 1 140 7 1 140 8 1 140 9 1 140 10 1 140 11 1 140 12 1
		 140 13 1 140 14 1 140 15 1 140 16 1 140 17 1 140 18 1 140 19 1 120 141 1 121 141 1
		 122 141 1 123 141 1 124 141 1 125 141 1 126 141 1 127 141 1 128 141 1 129 141 1 130 141 1
		 131 141 1 132 141 1 133 141 1 134 141 1 135 141 1 136 141 1 137 141 1 138 141 1 139 141 1;
	setAttr -size 160 -capacityHint 600 ".face[0:159]" -type "polyFaces" 
		f 4 0 141 -21 -141
		mu 0 4 20 21 42 41
		f 4 1 142 -22 -142
		mu 0 4 21 22 43 42
		f 4 2 143 -23 -143
		mu 0 4 22 23 44 43
		f 4 3 144 -24 -144
		mu 0 4 23 24 45 44
		f 4 4 145 -25 -145
		mu 0 4 24 25 46 45
		f 4 5 146 -26 -146
		mu 0 4 25 26 47 46
		f 4 6 147 -27 -147
		mu 0 4 26 27 48 47
		f 4 7 148 -28 -148
		mu 0 4 27 28 49 48
		f 4 8 149 -29 -149
		mu 0 4 28 29 50 49
		f 4 9 150 -30 -150
		mu 0 4 29 30 51 50
		f 4 10 151 -31 -151
		mu 0 4 30 31 52 51
		f 4 11 152 -32 -152
		mu 0 4 31 32 53 52
		f 4 12 153 -33 -153
		mu 0 4 32 33 54 53
		f 4 13 154 -34 -154
		mu 0 4 33 34 55 54
		f 4 14 155 -35 -155
		mu 0 4 34 35 56 55
		f 4 15 156 -36 -156
		mu 0 4 35 36 57 56
		f 4 16 157 -37 -157
		mu 0 4 36 37 58 57
		f 4 17 158 -38 -158
		mu 0 4 37 38 59 58
		f 4 18 159 -39 -159
		mu 0 4 38 39 60 59
		f 4 19 140 -40 -160
		mu 0 4 39 40 61 60
		f 4 20 161 -41 -161
		mu 0 4 41 42 63 62
		f 4 21 162 -42 -162
		mu 0 4 42 43 64 63
		f 4 22 163 -43 -163
		mu 0 4 43 44 65 64
		f 4 23 164 -44 -164
		mu 0 4 44 45 66 65
		f 4 24 165 -45 -165
		mu 0 4 45 46 67 66
		f 4 25 166 -46 -166
		mu 0 4 46 47 68 67
		f 4 26 167 -47 -167
		mu 0 4 47 48 69 68
		f 4 27 168 -48 -168
		mu 0 4 48 49 70 69
		f 4 28 169 -49 -169
		mu 0 4 49 50 71 70
		f 4 29 170 -50 -170
		mu 0 4 50 51 72 71
		f 4 30 171 -51 -171
		mu 0 4 51 52 73 72
		f 4 31 172 -52 -172
		mu 0 4 52 53 74 73
		f 4 32 173 -53 -173
		mu 0 4 53 54 75 74
		f 4 33 174 -54 -174
		mu 0 4 54 55 76 75
		f 4 34 175 -55 -175
		mu 0 4 55 56 77 76
		f 4 35 176 -56 -176
		mu 0 4 56 57 78 77
		f 4 36 177 -57 -177
		mu 0 4 57 58 79 78
		f 4 37 178 -58 -178
		mu 0 4 58 59 80 79
		f 4 38 179 -59 -179
		mu 0 4 59 60 81 80
		f 4 39 160 -60 -180
		mu 0 4 60 61 82 81
		f 4 40 181 -61 -181
		mu 0 4 62 63 84 83
		f 4 41 182 -62 -182
		mu 0 4 63 64 85 84
		f 4 42 183 -63 -183
		mu 0 4 64 65 86 85
		f 4 43 184 -64 -184
		mu 0 4 65 66 87 86
		f 4 44 185 -65 -185
		mu 0 4 66 67 88 87
		f 4 45 186 -66 -186
		mu 0 4 67 68 89 88
		f 4 46 187 -67 -187
		mu 0 4 68 69 90 89
		f 4 47 188 -68 -188
		mu 0 4 69 70 91 90
		f 4 48 189 -69 -189
		mu 0 4 70 71 92 91
		f 4 49 190 -70 -190
		mu 0 4 71 72 93 92
		f 4 50 191 -71 -191
		mu 0 4 72 73 94 93
		f 4 51 192 -72 -192
		mu 0 4 73 74 95 94
		f 4 52 193 -73 -193
		mu 0 4 74 75 96 95
		f 4 53 194 -74 -194
		mu 0 4 75 76 97 96
		f 4 54 195 -75 -195
		mu 0 4 76 77 98 97
		f 4 55 196 -76 -196
		mu 0 4 77 78 99 98
		f 4 56 197 -77 -197
		mu 0 4 78 79 100 99
		f 4 57 198 -78 -198
		mu 0 4 79 80 101 100
		f 4 58 199 -79 -199
		mu 0 4 80 81 102 101
		f 4 59 180 -80 -200
		mu 0 4 81 82 103 102
		f 4 60 201 -81 -201
		mu 0 4 83 84 105 104
		f 4 61 202 -82 -202
		mu 0 4 84 85 106 105
		f 4 62 203 -83 -203
		mu 0 4 85 86 107 106
		f 4 63 204 -84 -204
		mu 0 4 86 87 108 107
		f 4 64 205 -85 -205
		mu 0 4 87 88 109 108
		f 4 65 206 -86 -206
		mu 0 4 88 89 110 109
		f 4 66 207 -87 -207
		mu 0 4 89 90 111 110
		f 4 67 208 -88 -208
		mu 0 4 90 91 112 111
		f 4 68 209 -89 -209
		mu 0 4 91 92 113 112
		f 4 69 210 -90 -210
		mu 0 4 92 93 114 113
		f 4 70 211 -91 -211
		mu 0 4 93 94 115 114
		f 4 71 212 -92 -212
		mu 0 4 94 95 116 115
		f 4 72 213 -93 -213
		mu 0 4 95 96 117 116
		f 4 73 214 -94 -214
		mu 0 4 96 97 118 117
		f 4 74 215 -95 -215
		mu 0 4 97 98 119 118
		f 4 75 216 -96 -216
		mu 0 4 98 99 120 119
		f 4 76 217 -97 -217
		mu 0 4 99 100 121 120
		f 4 77 218 -98 -218
		mu 0 4 100 101 122 121
		f 4 78 219 -99 -219
		mu 0 4 101 102 123 122
		f 4 79 200 -100 -220
		mu 0 4 102 103 124 123
		f 4 80 221 -101 -221
		mu 0 4 104 105 126 125
		f 4 81 222 -102 -222
		mu 0 4 105 106 127 126
		f 4 82 223 -103 -223
		mu 0 4 106 107 128 127
		f 4 83 224 -104 -224
		mu 0 4 107 108 129 128
		f 4 84 225 -105 -225
		mu 0 4 108 109 130 129
		f 4 85 226 -106 -226
		mu 0 4 109 110 131 130
		f 4 86 227 -107 -227
		mu 0 4 110 111 132 131
		f 4 87 228 -108 -228
		mu 0 4 111 112 133 132
		f 4 88 229 -109 -229
		mu 0 4 112 113 134 133
		f 4 89 230 -110 -230
		mu 0 4 113 114 135 134
		f 4 90 231 -111 -231
		mu 0 4 114 115 136 135
		f 4 91 232 -112 -232
		mu 0 4 115 116 137 136
		f 4 92 233 -113 -233
		mu 0 4 116 117 138 137
		f 4 93 234 -114 -234
		mu 0 4 117 118 139 138
		f 4 94 235 -115 -235
		mu 0 4 118 119 140 139
		f 4 95 236 -116 -236
		mu 0 4 119 120 141 140
		f 4 96 237 -117 -237
		mu 0 4 120 121 142 141
		f 4 97 238 -118 -238
		mu 0 4 121 122 143 142
		f 4 98 239 -119 -239
		mu 0 4 122 123 144 143
		f 4 99 220 -120 -240
		mu 0 4 123 124 145 144
		f 4 100 241 -121 -241
		mu 0 4 125 126 147 146
		f 4 101 242 -122 -242
		mu 0 4 126 127 148 147
		f 4 102 243 -123 -243
		mu 0 4 127 128 149 148
		f 4 103 244 -124 -244
		mu 0 4 128 129 150 149
		f 4 104 245 -125 -245
		mu 0 4 129 130 151 150
		f 4 105 246 -126 -246
		mu 0 4 130 131 152 151
		f 4 106 247 -127 -247
		mu 0 4 131 132 153 152
		f 4 107 248 -128 -248
		mu 0 4 132 133 154 153
		f 4 108 249 -129 -249
		mu 0 4 133 134 155 154
		f 4 109 250 -130 -250
		mu 0 4 134 135 156 155
		f 4 110 251 -131 -251
		mu 0 4 135 136 157 156
		f 4 111 252 -132 -252
		mu 0 4 136 137 158 157
		f 4 112 253 -133 -253
		mu 0 4 137 138 159 158
		f 4 113 254 -134 -254
		mu 0 4 138 139 160 159
		f 4 114 255 -135 -255
		mu 0 4 139 140 161 160
		f 4 115 256 -136 -256
		mu 0 4 140 141 162 161
		f 4 116 257 -137 -257
		mu 0 4 141 142 163 162
		f 4 117 258 -138 -258
		mu 0 4 142 143 164 163
		f 4 118 259 -139 -259
		mu 0 4 143 144 165 164
		f 4 119 240 -140 -260
		mu 0 4 144 145 166 165
		f 3 -1 -261 261
		mu 0 3 1 0 187
		f 3 -2 -262 262
		mu 0 3 2 1 187
		f 3 -3 -263 263
		mu 0 3 3 2 187
		f 3 -4 -264 264
		mu 0 3 4 3 187
		f 3 -5 -265 265
		mu 0 3 5 4 187
		f 3 -6 -266 266
		mu 0 3 6 5 187
		f 3 -7 -267 267
		mu 0 3 7 6 187
		f 3 -8 -268 268
		mu 0 3 8 7 187
		f 3 -9 -269 269
		mu 0 3 9 8 187
		f 3 -10 -270 270
		mu 0 3 10 9 187
		f 3 -11 -271 271
		mu 0 3 11 10 187
		f 3 -12 -272 272
		mu 0 3 12 11 187
		f 3 -13 -273 273
		mu 0 3 13 12 187
		f 3 -14 -274 274
		mu 0 3 14 13 187
		f 3 -15 -275 275
		mu 0 3 15 14 187
		f 3 -16 -276 276
		mu 0 3 16 15 187
		f 3 -17 -277 277
		mu 0 3 17 16 187
		f 3 -18 -278 278
		mu 0 3 18 17 187
		f 3 -19 -279 279
		mu 0 3 19 18 187
		f 3 -20 -280 260
		mu 0 3 0 19 187
		f 3 120 281 -281
		mu 0 3 185 184 188
		f 3 121 282 -282
		mu 0 3 184 183 188
		f 3 122 283 -283
		mu 0 3 183 182 188
		f 3 123 284 -284
		mu 0 3 182 181 188
		f 3 124 285 -285
		mu 0 3 181 180 188
		f 3 125 286 -286
		mu 0 3 180 179 188
		f 3 126 287 -287
		mu 0 3 179 178 188
		f 3 127 288 -288
		mu 0 3 178 177 188
		f 3 128 289 -289
		mu 0 3 177 176 188
		f 3 129 290 -290
		mu 0 3 176 175 188
		f 3 130 291 -291
		mu 0 3 175 174 188
		f 3 131 292 -292
		mu 0 3 174 173 188
		f 3 132 293 -293
		mu 0 3 173 172 188
		f 3 133 294 -294
		mu 0 3 172 171 188
		f 3 134 295 -295
		mu 0 3 171 170 188
		f 3 135 296 -296
		mu 0 3 170 169 188
		f 3 136 297 -297
		mu 0 3 169 168 188
		f 3 137 298 -298
		mu 0 3 168 167 188
		f 3 138 299 -299
		mu 0 3 167 186 188
		f 3 139 280 -300
		mu 0 3 186 185 188;
	setAttr ".creaseData" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".creaseVertexData" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pinData[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".holeFaceData" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".vertexColorSource" 2;
createNode lightLinker -shared -name "lightLinker1";
	rename -uuid "024A7028-4F2A-3815-8987-7BA122403FEF";
	setAttr -size 3 ".link";
	setAttr -size 3 ".shadowLink";
createNode shapeEditorManager -name "shapeEditorManager";
	rename -uuid "4300C23B-4269-AF74-918F-199716FF919A";
createNode poseInterpolatorManager -name "poseInterpolatorManager";
	rename -uuid "04576F16-4738-3E52-8D74-459E12944FA9";
createNode displayLayerManager -name "layerManager";
	rename -uuid "70D94189-4678-A3FE-AC70-349FAFDE4226";
createNode displayLayer -name "defaultLayer";
	rename -uuid "B0B57F93-452D-2502-78E9-2B8D332D397D";
createNode renderLayerManager -name "renderLayerManager";
	rename -uuid "758EBB3E-4BBE-0947-69FF-A8AA4B32930C";
createNode renderLayer -name "defaultRenderLayer";
	rename -uuid "9EF1CBFA-4821-263B-2CEE-A091E0255C31";
	setAttr ".global" yes;
createNode aiOptions -shared -name "defaultArnoldRenderOptions";
	rename -uuid "1220C71B-47F2-5442-3440-C68AA2814052";
	setAttr ".version" -type "string" "5.3.1.1";
createNode aiAOVFilter -shared -name "defaultArnoldFilter";
	rename -uuid "EFCD5F6B-4FA9-0D1D-F135-D491DB6FC9B4";
	setAttr ".aiTranslator" -type "string" "gaussian";
createNode aiAOVDriver -shared -name "defaultArnoldDriver";
	rename -uuid "B25FCDC5-4484-EC8F-3B1A-7299DB5D44F4";
	setAttr ".aiTranslator" -type "string" "exr";
createNode aiAOVDriver -shared -name "defaultArnoldDisplayDriver";
	rename -uuid "E60105A2-4870-404C-AE38-31846C5076DC";
	setAttr ".outputMode" 0;
	setAttr ".aiTranslator" -type "string" "maya";
createNode polyCylinder -name "polyCylinder1";
	rename -uuid "58CC1881-4E5D-2186-3D1D-84808E91ADC5";
	setAttr ".height" 6;
	setAttr ".subdivisionsHeight" 6;
	setAttr ".subdivisionsCaps" 1;
	setAttr ".createUVs" 3;
createNode skinCluster -name "skinCluster1";
	rename -uuid "ADD18122-4B43-1BE2-EF8A-1DA88EE9CB2F";
	setAttr -size 142 ".weightList";
	setAttr ".weightList[0:141].weights"
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		2 1 0.5 2 0.5
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 0 1
		1 2 1;
	setAttr -size 3 ".bindPreMatrix";
	setAttr ".bindPreMatrix[0]" -type "matrix" 0 -1 0 0 1 0 0 0 0 0 1 0 0 0 0 1;
	setAttr ".bindPreMatrix[1]" -type "matrix" 0 -1 0 0 1 0 0 0 0 0 1 0 -2 0 0 1;
	setAttr ".bindPreMatrix[2]" -type "matrix" 0 -1 0 0 1 0 0 0 0 0 1 0 -4 0 0 1;
	setAttr ".geomMatrix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 3 0 1;
	setAttr -size 3 ".matrix";
	setAttr -size 3 ".dropoff[0:2]"  4 4 4;
	setAttr -size 3 ".lockWeights";
	setAttr -size 3 ".lockWeights";
	setAttr ".maintainMaxInfluences" yes;
	setAttr ".useComponentsMatrix" yes;
	setAttr -size 3 ".influenceColor";
	setAttr -size 3 ".influenceColor";
createNode dagPose -name "bindPose1";
	rename -uuid "2CE88AA4-4287-E4D5-D52E-47ACAF7FCA08";
	setAttr -size 5 ".worldMatrix";
	setAttr ".worldMatrix[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".worldMatrix[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -size 5 ".xformMatrix";
	setAttr ".xformMatrix[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xformMatrix[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xformMatrix[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0.70710678118654757 0.70710678118654757 1 1 1 yes;
	setAttr ".xformMatrix[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 2 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xformMatrix[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 2 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr -size 5 ".members";
	setAttr -size 5 ".parents";
	setAttr -size 5 ".global[0:4]" yes yes no no no;
	setAttr ".bindPose" yes;
createNode script -name "sceneConfigurationScriptNode";
	rename -uuid "159C945F-42E8-158C-9D2E-338A41CD6EDE";
	setAttr ".before" -type "string" "playbackOptions -min 0 -max 150 -ast 0 -aet 150 ";
	setAttr ".scriptType" 6;
createNode deltaMush -name "deltaMush1";
	rename -uuid "8A069AA7-425A-6192-659F-0ABA804498AA";
	setAttr ".smoothingIterations" 5;
	setAttr ".smoothingStep" 0.60000002384185791;
	setAttr ".inwardConstraint" 1;
createNode nodeGraphEditorInfo -name "MayaNodeEditorSavedTabsInfo";
	rename -uuid "251F3452-41C6-5A55-307F-A68965CCF688";
	setAttr ".tabGraphInfo[0].tabName" -type "string" "Untitled_1";
	setAttr ".tabGraphInfo[0].viewRectLow" -type "double2" -499.68485982944719 -243.87254233917042 ;
	setAttr ".tabGraphInfo[0].viewRectHigh" -type "double2" 481.82771768188337 271.25349363210154 ;
	setAttr -size 3 ".tabGraphInfo[0].nodeInfo";
	setAttr ".tabGraphInfo[0].nodeInfo[0].positionX" 47.142856597900391;
	setAttr ".tabGraphInfo[0].nodeInfo[0].positionY" 170;
	setAttr ".tabGraphInfo[0].nodeInfo[0].nodeVisualState" 18304;
	setAttr ".tabGraphInfo[0].nodeInfo[1].positionX" 47.142856597900391;
	setAttr ".tabGraphInfo[0].nodeInfo[1].positionY" 40;
	setAttr ".tabGraphInfo[0].nodeInfo[1].nodeVisualState" 18304;
	setAttr ".tabGraphInfo[0].nodeInfo[2].positionX" -260;
	setAttr ".tabGraphInfo[0].nodeInfo[2].positionY" 170;
	setAttr ".tabGraphInfo[0].nodeInfo[2].nodeVisualState" 18304;
createNode skinCluster -name "skinCluster2";
	rename -uuid "38FDD45E-4726-E3C7-5E90-41A8A2FA5A48";
	setAttr -size 142 ".weightList";
	setAttr ".weightList[0:141].weights"
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		2 1 1 2 -1.5625535738844279e-16
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 0 1
		1 2 1;
	setAttr -size 3 ".bindPreMatrix";
	setAttr ".bindPreMatrix[0]" -type "matrix" 0 -1 0 0 1 0 0 0 0 0 1 0 0 0 0 1;
	setAttr ".bindPreMatrix[1]" -type "matrix" 0 -1 0 0 1 0 0 0 0 0 1 0 -2 0 0 1;
	setAttr ".bindPreMatrix[2]" -type "matrix" 0 -1 0 0 1 0 0 0 0 0 1 0 -4 0 0 1;
	setAttr ".geomMatrix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 3 0 1;
	setAttr -size 3 ".matrix";
	setAttr -size 3 ".dropoff[0:2]"  4 4 4;
	setAttr -size 3 ".lockWeights";
	setAttr -size 3 ".lockWeights";
	setAttr ".maintainMaxInfluences" yes;
	setAttr ".useComponentsMatrix" yes;
	setAttr -size 3 ".influenceColor";
	setAttr -size 3 ".influenceColor";
createNode shadingEngine -name "lambert1SG";
	rename -uuid "261C1EA2-422B-03F7-AD6D-3BA0A5F9F38F";
	setAttr ".isHistoricallyInteresting" 0;
	setAttr -size 2 ".dagSetMembers";
	setAttr ".renderableOnlySet" yes;
createNode materialInfo -name "materialInfo1";
	rename -uuid "50276A89-46BD-0A08-FC00-7FB47ADD0685";
createNode nodeGraphEditorInfo -name "hyperShadePrimaryNodeEditorSavedTabsInfo";
	rename -uuid "8A2817CF-4344-DD52-FB79-E6BDCF062204";
	setAttr ".tabGraphInfo[0].tabName" -type "string" "Untitled_1";
	setAttr ".tabGraphInfo[0].viewRectLow" -type "double2" -330.95236780151544 -323.80951094248991 ;
	setAttr ".tabGraphInfo[0].viewRectHigh" -type "double2" 317.85713022663526 338.09522466054096 ;
	setAttr -size 33 ".tabGraphInfo[0].nodeInfo";
	setAttr ".tabGraphInfo[0].nodeInfo[0].positionX" -2435.71435546875;
	setAttr ".tabGraphInfo[0].nodeInfo[0].positionY" 655.71429443359375;
	setAttr ".tabGraphInfo[0].nodeInfo[0].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[1].positionX" 1922.857177734375;
	setAttr ".tabGraphInfo[0].nodeInfo[1].positionY" 464.28570556640625;
	setAttr ".tabGraphInfo[0].nodeInfo[1].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[2].positionX" 1922.857177734375;
	setAttr ".tabGraphInfo[0].nodeInfo[2].positionY" 222.85714721679688;
	setAttr ".tabGraphInfo[0].nodeInfo[2].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[3].positionX" 1601.4285888671875;
	setAttr ".tabGraphInfo[0].nodeInfo[3].positionY" 371.42855834960938;
	setAttr ".tabGraphInfo[0].nodeInfo[3].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[4].positionX" 1601.4285888671875;
	setAttr ".tabGraphInfo[0].nodeInfo[4].positionY" 612.85711669921875;
	setAttr ".tabGraphInfo[0].nodeInfo[4].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[5].positionX" 1601.4285888671875;
	setAttr ".tabGraphInfo[0].nodeInfo[5].positionY" 187.14285278320312;
	setAttr ".tabGraphInfo[0].nodeInfo[5].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[6].positionX" 1922.857177734375;
	setAttr ".tabGraphInfo[0].nodeInfo[6].positionY" 705.71429443359375;
	setAttr ".tabGraphInfo[0].nodeInfo[6].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[7].positionX" 1601.4285888671875;
	setAttr ".tabGraphInfo[0].nodeInfo[7].positionY" 774.28570556640625;
	setAttr ".tabGraphInfo[0].nodeInfo[7].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[8].positionX" 1922.857177734375;
	setAttr ".tabGraphInfo[0].nodeInfo[8].positionY" 70;
	setAttr ".tabGraphInfo[0].nodeInfo[8].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[9].positionX" -2128.571533203125;
	setAttr ".tabGraphInfo[0].nodeInfo[9].positionY" 585.71429443359375;
	setAttr ".tabGraphInfo[0].nodeInfo[9].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[10].positionX" 1922.857177734375;
	setAttr ".tabGraphInfo[0].nodeInfo[10].positionY" -258.57144165039062;
	setAttr ".tabGraphInfo[0].nodeInfo[10].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[11].positionX" 1922.857177734375;
	setAttr ".tabGraphInfo[0].nodeInfo[11].positionY" -442.85714721679688;
	setAttr ".tabGraphInfo[0].nodeInfo[11].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[12].positionX" 1250;
	setAttr ".tabGraphInfo[0].nodeInfo[12].positionY" 170;
	setAttr ".tabGraphInfo[0].nodeInfo[12].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[13].positionX" 1922.857177734375;
	setAttr ".tabGraphInfo[0].nodeInfo[13].positionY" -82.857139587402344;
	setAttr ".tabGraphInfo[0].nodeInfo[13].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[14].positionX" 2238.571533203125;
	setAttr ".tabGraphInfo[0].nodeInfo[14].positionY" 762.85711669921875;
	setAttr ".tabGraphInfo[0].nodeInfo[14].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[15].positionX" 2238.571533203125;
	setAttr ".tabGraphInfo[0].nodeInfo[15].positionY" 521.4285888671875;
	setAttr ".tabGraphInfo[0].nodeInfo[15].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[16].positionX" 942.85711669921875;
	setAttr ".tabGraphInfo[0].nodeInfo[16].positionY" 74.285713195800781;
	setAttr ".tabGraphInfo[0].nodeInfo[16].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[17].positionX" 2238.571533203125;
	setAttr ".tabGraphInfo[0].nodeInfo[17].positionY" 280;
	setAttr ".tabGraphInfo[0].nodeInfo[17].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[18].positionX" 21.428571701049805;
	setAttr ".tabGraphInfo[0].nodeInfo[18].positionY" 764.28570556640625;
	setAttr ".tabGraphInfo[0].nodeInfo[18].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[19].positionX" 635.71429443359375;
	setAttr ".tabGraphInfo[0].nodeInfo[19].positionY" 774.28570556640625;
	setAttr ".tabGraphInfo[0].nodeInfo[19].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[20].positionX" 328.57144165039062;
	setAttr ".tabGraphInfo[0].nodeInfo[20].positionY" 684.28570556640625;
	setAttr ".tabGraphInfo[0].nodeInfo[20].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[21].positionX" -285.71429443359375;
	setAttr ".tabGraphInfo[0].nodeInfo[21].positionY" 674.28570556640625;
	setAttr ".tabGraphInfo[0].nodeInfo[21].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[22].positionX" -900;
	setAttr ".tabGraphInfo[0].nodeInfo[22].positionY" 774.28570556640625;
	setAttr ".tabGraphInfo[0].nodeInfo[22].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[23].positionX" -1207.142822265625;
	setAttr ".tabGraphInfo[0].nodeInfo[23].positionY" 717.14288330078125;
	setAttr ".tabGraphInfo[0].nodeInfo[23].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[24].positionX" -1514.2857666015625;
	setAttr ".tabGraphInfo[0].nodeInfo[24].positionY" 725.71429443359375;
	setAttr ".tabGraphInfo[0].nodeInfo[24].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[25].positionX" 942.85711669921875;
	setAttr ".tabGraphInfo[0].nodeInfo[25].positionY" 797.14288330078125;
	setAttr ".tabGraphInfo[0].nodeInfo[25].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[26].positionX" -1821.4285888671875;
	setAttr ".tabGraphInfo[0].nodeInfo[26].positionY" 650;
	setAttr ".tabGraphInfo[0].nodeInfo[26].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[27].positionX" 1601.4285888671875;
	setAttr ".tabGraphInfo[0].nodeInfo[27].positionY" -445.71429443359375;
	setAttr ".tabGraphInfo[0].nodeInfo[27].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[28].positionX" -592.85711669921875;
	setAttr ".tabGraphInfo[0].nodeInfo[28].positionY" 688.5714111328125;
	setAttr ".tabGraphInfo[0].nodeInfo[28].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[29].positionX" 1922.857177734375;
	setAttr ".tabGraphInfo[0].nodeInfo[29].positionY" -655.71429443359375;
	setAttr ".tabGraphInfo[0].nodeInfo[29].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[30].positionX" 2238.571533203125;
	setAttr ".tabGraphInfo[0].nodeInfo[30].positionY" -82.857139587402344;
	setAttr ".tabGraphInfo[0].nodeInfo[30].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[31].positionX" 1250;
	setAttr ".tabGraphInfo[0].nodeInfo[31].positionY" 522.85711669921875;
	setAttr ".tabGraphInfo[0].nodeInfo[31].nodeVisualState" 1922;
	setAttr ".tabGraphInfo[0].nodeInfo[32].positionX" -98.571426391601562;
	setAttr ".tabGraphInfo[0].nodeInfo[32].positionY" 81.428573608398438;
	setAttr ".tabGraphInfo[0].nodeInfo[32].nodeVisualState" 1923;
select -noExpand :time1;
	setAttr -alteredValue -keyable on ".caching";
	setAttr -keyable on ".frozen";
	setAttr -alteredValue -channelBox on ".isHistoricallyInteresting";
	setAttr -alteredValue -keyable on ".nodeState";
	setAttr -channelBox on ".binMembership";
	setAttr -keyable on ".outTime" 0;
	setAttr -alteredValue -keyable on ".unwarpedTime";
	setAttr -alteredValue -keyable on ".enableTimewarp";
	setAttr -alteredValue -keyable on ".timecodeProductionStart";
	setAttr -alteredValue -keyable on ".timecodeMayaStart";
select -noExpand :hardwareRenderingGlobals;
	setAttr -alteredValue -keyable on ".caching";
	setAttr -alteredValue -keyable on ".isHistoricallyInteresting";
	setAttr -alteredValue -keyable on ".nodeState";
	setAttr -channelBox on ".binMembership";
	setAttr ".objectTypeFilterNameArray" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".objectTypeFilterValueArray" -type "Int32Array" 22 0 1 1
		 1 1 1 1 1 1 0 0 0 0 0 0
		 0 0 0 0 0 0 0 ;
	setAttr -keyable on ".hwInstancing";
	setAttr -alteredValue ".transparencyAlgorithm";
	setAttr -alteredValue ".transparencyQuality";
	setAttr -alteredValue ".enableTextureMaxRes";
	setAttr -alteredValue ".textureMaxResolution";
	setAttr -alteredValue ".ssaoEnable";
	setAttr -alteredValue ".ssaoAmount";
	setAttr -alteredValue ".ssaoRadius";
	setAttr -keyable on ".hwFogFalloff";
	setAttr -alteredValue -keyable on ".hwFogDensity";
	setAttr -alteredValue -keyable on ".hwFogStart";
	setAttr -alteredValue -keyable on ".hwFogEnd";
	setAttr -alteredValue ".hwFogColor";
	setAttr -alteredValue -keyable on ".hwFogColorR";
	setAttr -alteredValue -keyable on ".hwFogColorG";
	setAttr -alteredValue -keyable on ".hwFogColorB";
	setAttr -alteredValue -keyable on ".hwFogAlpha";
	setAttr -alteredValue ".motionBlurEnable";
	setAttr -alteredValue -keyable on ".motionBlurShutterOpenFraction";
	setAttr -keyable on ".bloomEnable";
	setAttr -keyable on ".bloomAmount";
	setAttr -alteredValue ".multiSampleEnable";
select -noExpand :renderPartition;
	setAttr -alteredValue -keyable on ".caching";
	setAttr -channelBox on ".isHistoricallyInteresting";
	setAttr -alteredValue -keyable on ".nodeState";
	setAttr -channelBox on ".binMembership";
	setAttr -size 3 ".sets";
	setAttr -channelBox on ".annotation";
	setAttr -channelBox on ".partitionType";
select -noExpand :renderGlobalsList1;
	setAttr -keyable on ".caching";
	setAttr -channelBox on ".isHistoricallyInteresting";
	setAttr -keyable on ".nodeState";
	setAttr -channelBox on ".binMembership";
select -noExpand :defaultShaderList1;
	setAttr -keyable on ".caching";
	setAttr -channelBox on ".isHistoricallyInteresting";
	setAttr -keyable on ".nodeState";
	setAttr -channelBox on ".binMembership";
	setAttr -size 5 ".shaders";
select -noExpand :postProcessList1;
	setAttr -keyable on ".caching";
	setAttr -channelBox on ".isHistoricallyInteresting";
	setAttr -keyable on ".nodeState";
	setAttr -channelBox on ".binMembership";
	setAttr -size 2 ".postProcesses";
select -noExpand :defaultRenderingList1;
	setAttr -keyable on ".isHistoricallyInteresting";
select -noExpand :standardSurface1;
	setAttr ".baseColor" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".specularRoughness" 0.5;
select -noExpand :initialShadingGroup;
	setAttr -alteredValue -keyable on ".caching";
	setAttr -keyable on ".frozen";
	setAttr -channelBox on ".isHistoricallyInteresting";
	setAttr -alteredValue -keyable on ".nodeState";
	setAttr -channelBox on ".binMembership";
	setAttr -keyable on ".blackBox";
	setAttr -keyable on ".viewMode";
	setAttr -keyable on ".templateVersion";
	setAttr -keyable on ".uiTreatment";
	setAttr -keyable on ".memberWireframeColor";
	setAttr -alteredValue -channelBox on ".annotation";
	setAttr -channelBox on ".isLayer";
	setAttr -channelBox on ".verticesOnlySet";
	setAttr -channelBox on ".edgesOnlySet";
	setAttr -channelBox on ".facetsOnlySet";
	setAttr -channelBox on ".editPointsOnlySet";
	setAttr -keyable on ".renderableOnlySet" yes;
	setAttr -channelBox on ".aiOverride";
	setAttr -keyable on ".aiSurfaceShader";
	setAttr -channelBox on ".aiSurfaceShaderR";
	setAttr -channelBox on ".aiSurfaceShaderG";
	setAttr -channelBox on ".aiSurfaceShaderB";
	setAttr -keyable on ".aiVolumeShader";
	setAttr -channelBox on ".aiVolumeShaderR";
	setAttr -channelBox on ".aiVolumeShaderG";
	setAttr -channelBox on ".aiVolumeShaderB";
select -noExpand :initialParticleSE;
	setAttr -alteredValue -keyable on ".caching";
	setAttr -channelBox on ".isHistoricallyInteresting";
	setAttr -alteredValue -keyable on ".nodeState";
	setAttr -channelBox on ".binMembership";
	setAttr -keyable on ".memberWireframeColor";
	setAttr -channelBox on ".annotation";
	setAttr -channelBox on ".isLayer";
	setAttr -channelBox on ".verticesOnlySet";
	setAttr -channelBox on ".edgesOnlySet";
	setAttr -channelBox on ".facetsOnlySet";
	setAttr -channelBox on ".editPointsOnlySet";
	setAttr -keyable on ".renderableOnlySet" yes;
	setAttr -channelBox on ".aiOverride";
	setAttr -keyable on ".aiSurfaceShader";
	setAttr -channelBox on ".aiSurfaceShaderR";
	setAttr -channelBox on ".aiSurfaceShaderG";
	setAttr -channelBox on ".aiSurfaceShaderB";
	setAttr -keyable on ".aiVolumeShader";
	setAttr -channelBox on ".aiVolumeShaderR";
	setAttr -channelBox on ".aiVolumeShaderG";
	setAttr -channelBox on ".aiVolumeShaderB";
select -noExpand :initialMaterialInfo;
select -noExpand :defaultRenderGlobals;
	addAttr -cachedInternally true -hidden true -shortName "dss" -longName "defaultSurfaceShader" 
		-dataType "string";
	setAttr -alteredValue -keyable on ".caching";
	setAttr -channelBox on ".isHistoricallyInteresting";
	setAttr -alteredValue -keyable on ".nodeState";
	setAttr -channelBox on ".binMembership";
	setAttr -alteredValue -keyable on ".macCodec";
	setAttr -alteredValue -keyable on ".macDepth";
	setAttr -alteredValue -keyable on ".macQual";
	setAttr -alteredValue -keyable on ".comFrrt";
	setAttr -channelBox on ".ignoreFilmGate";
	setAttr -alteredValue -keyable on ".clipFinalShadedColor";
	setAttr -alteredValue -keyable on ".enableDepthMaps";
	setAttr -alteredValue -keyable on ".enableDefaultLight";
	setAttr -alteredValue -channelBox on ".currentRenderer" -type "string" "arnold";
	setAttr -alteredValue -keyable on ".enableStrokeRender";
	setAttr -alteredValue -keyable on ".onlyRenderStrokes";
	setAttr -channelBox on ".strokesDepthFile";
	setAttr -alteredValue -keyable on ".imageFormat";
	setAttr -alteredValue -channelBox on ".imfPluginKey";
	setAttr -alteredValue -keyable on ".gammaCorrection";
	setAttr -alteredValue -keyable on ".exrCompression";
	setAttr -alteredValue -keyable on ".exrPixelType";
	setAttr -alteredValue -keyable on ".animation";
	setAttr -channelBox on ".animationRange";
	setAttr -alteredValue -keyable on ".startFrame" 1;
	setAttr -alteredValue -keyable on ".endFrame" 10;
	setAttr -alteredValue -keyable on ".byFrameStep";
	setAttr -alteredValue -channelBox on ".modifyExtension";
	setAttr -channelBox on ".startExtension";
	setAttr -alteredValue -keyable on ".byExtension";
	setAttr -alteredValue -channelBox on ".extensionPadding";
	setAttr -alteredValue -keyable on ".fieldExtControl";
	setAttr -alteredValue -keyable on ".outFormatControl";
	setAttr -channelBox on ".oddFieldExt";
	setAttr -channelBox on ".evenFieldExt";
	setAttr -channelBox on ".outFormatExt";
	setAttr -channelBox on ".useMayaFileName";
	setAttr -channelBox on ".useFrameExt";
	setAttr -alteredValue -channelBox on ".putFrameBeforeExt";
	setAttr -alteredValue -channelBox on ".periodInExt";
	setAttr -alteredValue -channelBox on ".imageFilePrefix";
	setAttr -keyable on ".renderVersion";
	setAttr -alteredValue -keyable on ".composite";
	setAttr -alteredValue -keyable on ".compositeThreshold";
	setAttr -alteredValue -keyable on ".shadowsObeyLightLinking";
	setAttr -alteredValue -channelBox on ".shadowsObeyShadowLinking";
	setAttr -alteredValue -keyable on ".recursionDepth";
	setAttr -alteredValue -keyable on ".leafPrimitives";
	setAttr -alteredValue -keyable on ".subdivisionPower";
	setAttr -alteredValue -keyable on ".subdivisionHashSize";
	setAttr -alteredValue -keyable on ".logRenderPerformance";
	setAttr -channelBox on ".geometryVector";
	setAttr -channelBox on ".shadingVector";
	setAttr -alteredValue -keyable on ".maximumMemory";
	setAttr -alteredValue -keyable on ".numCpusToUse";
	setAttr -alteredValue -keyable on ".interruptFrequency";
	setAttr -alteredValue -keyable on ".shadowPass";
	setAttr -channelBox on ".iprShadowPass";
	setAttr -alteredValue -keyable on ".useFileCache";
	setAttr -alteredValue -keyable on ".optimizeInstances";
	setAttr -alteredValue -keyable on ".reuseTessellations";
	setAttr -alteredValue -keyable on ".matteOpacityUsesTransparency";
	setAttr -alteredValue -channelBox on ".motionBlur";
	setAttr -alteredValue -keyable on ".motionBlurByFrame";
	setAttr -alteredValue -keyable on ".motionBlurShutterOpen";
	setAttr -alteredValue -keyable on ".motionBlurShutterClose";
	setAttr -alteredValue -keyable on ".applyFogInPost";
	setAttr -alteredValue -keyable on ".postFogBlur";
	setAttr -alteredValue -keyable on ".preMel";
	setAttr -alteredValue -keyable on ".postMel";
	setAttr -alteredValue -keyable on ".preRenderLayerMel";
	setAttr -alteredValue -keyable on ".postRenderLayerMel";
	setAttr -alteredValue -channelBox on ".preRenderMel";
	setAttr -alteredValue -channelBox on ".postRenderMel";
	setAttr -channelBox on ".preFurRenderMel";
	setAttr -channelBox on ".postFurRenderMel";
	setAttr -alteredValue -keyable on ".blurLength";
	setAttr -alteredValue -keyable on ".blurSharpness";
	setAttr -alteredValue -keyable on ".smoothValue";
	setAttr -alteredValue -keyable on ".useBlur2DMemoryCap";
	setAttr -alteredValue -keyable on ".blur2DMemoryCap";
	setAttr -channelBox on ".motionBlurType";
	setAttr -alteredValue -keyable on ".useDisplacementBoundingBox";
	setAttr -alteredValue -keyable on ".smoothColor";
	setAttr -alteredValue -keyable on ".keepMotionVector";
	setAttr -channelBox on ".iprRenderShading";
	setAttr -channelBox on ".iprRenderShadowMaps";
	setAttr -channelBox on ".iprRenderMotionBlur";
	setAttr -alteredValue -keyable on ".renderLayerEnable";
	setAttr -alteredValue -keyable on ".forceTileSize";
	setAttr -alteredValue -keyable on ".tileWidth";
	setAttr -alteredValue -keyable on ".tileHeight";
	setAttr -alteredValue -keyable on ".jitterFinalColor";
	setAttr -channelBox on ".raysSeeBackground";
	setAttr -alteredValue -keyable on ".oversamplePaintEffects";
	setAttr -alteredValue -keyable on ".oversamplePfxPostFilter";
	setAttr -alteredValue -keyable on ".renderingColorProfile";
	setAttr -alteredValue -keyable on ".inputColorProfile";
	setAttr -alteredValue -keyable on ".outputColorProfile";
	setAttr -channelBox on ".hyperShadeBinList";
	setAttr ".defaultSurfaceShader" -type "string" "standardSurface1";
select -noExpand :defaultResolution;
	setAttr -alteredValue -keyable on ".caching";
	setAttr -alteredValue -keyable on ".isHistoricallyInteresting";
	setAttr -alteredValue -keyable on ".nodeState";
	setAttr -keyable on ".binMembership";
	setAttr -alteredValue -keyable on ".width";
	setAttr -alteredValue -keyable on ".height";
	setAttr -alteredValue -keyable on ".pixelAspect" 1;
	setAttr -alteredValue -keyable on ".aspectLock";
	setAttr -alteredValue -keyable on ".deviceAspectRatio";
	setAttr -alteredValue -keyable on ".lockDeviceAspectRatio";
	setAttr -alteredValue -keyable on ".dotsPerInch";
	setAttr -alteredValue -keyable on ".oddFieldFirst";
	setAttr -alteredValue -keyable on ".fields";
	setAttr -alteredValue -keyable on ".zerothScanline";
	setAttr -alteredValue -keyable on ".imageSizeUnits";
	setAttr -alteredValue -keyable on ".pixelDensityUnits";
select -noExpand :defaultColorMgtGlobals;
	setAttr ".cmEnabled" no;
	setAttr ".configFileEnabled" yes;
	setAttr ".configFilePath" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".viewTransformName" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".viewName" -type "string" "ACES 1.0 SDR-video";
	setAttr ".displayName" -type "string" "sRGB";
	setAttr ".workingSpaceName" -type "string" "ACEScg";
	setAttr ".outputTransformName" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".playblastOutputTransformName" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -noExpand :hardwareRenderGlobals;
	setAttr -alteredValue -keyable on ".caching";
	setAttr -channelBox on ".isHistoricallyInteresting";
	setAttr -alteredValue -keyable on ".nodeState";
	setAttr -channelBox on ".binMembership";
	setAttr -alteredValue -keyable off -channelBox on ".colorTextureResolution" 256;
	setAttr -alteredValue -keyable off -channelBox on ".bumpTextureResolution" 512;
	setAttr -alteredValue -keyable off -channelBox on ".frameBufferFormat";
	setAttr -alteredValue -keyable off -channelBox on ".enableHighQualityLighting";
	setAttr -alteredValue -keyable off -channelBox on ".enableAcceleratedMultiSampling";
	setAttr -alteredValue -keyable off -channelBox on ".enableEdgeAntiAliasing";
	setAttr -alteredValue -keyable off -channelBox on ".enableGeometryMask";
	setAttr -alteredValue -keyable off -channelBox on ".numberOfSamples";
	setAttr -alteredValue -keyable off -channelBox on ".enableMotionBlur";
	setAttr -alteredValue -keyable off -channelBox on ".motionBlurByFrame";
	setAttr -alteredValue -keyable off -channelBox on ".numberOfExposures";
	setAttr -alteredValue -keyable off -channelBox on ".transparencySorting";
	setAttr -alteredValue -keyable off -channelBox on ".transparentShadowCasting";
	setAttr -alteredValue -keyable off -channelBox on ".enableNonPowerOfTwoTexture";
	setAttr -alteredValue -keyable off -channelBox on ".culling";
	setAttr -alteredValue -keyable off -channelBox on ".textureCompression";
	setAttr -alteredValue -keyable off -channelBox on ".lightIntensityThreshold";
	setAttr -alteredValue -keyable off -channelBox on ".smallObjectCulling";
	setAttr -alteredValue -keyable off -channelBox on ".cullingThreshold";
	setAttr -alteredValue -keyable off -channelBox on ".graphicsHardwareGeometryCachingData";
	setAttr -alteredValue -keyable off -channelBox on ".graphicsHardwareGeometryCachingIndexing";
	setAttr -alteredValue -keyable off -channelBox on ".maximumGeometryCacheSize";
	setAttr -alteredValue -keyable off -channelBox on ".writeAlphaAsColor";
	setAttr -alteredValue -keyable off -channelBox on ".writeZDepthAsColor";
	setAttr -keyable on ".hardwareCodec";
	setAttr -keyable on ".hardwareDepth";
	setAttr -keyable on ".hardwareQual";
	setAttr -keyable on ".hardwareFrameRate";
	setAttr -keyable on ".shadowsObeyLightLinking";
	setAttr -keyable on ".shadowsObeyShadowLinking";
	setAttr -keyable on ".blendSpecularWithAlpha";
	setAttr -keyable on ".shadingModel";
	setAttr -keyable on ".hardwareEnvironmentLookup";
connectAttr "deltaMush1.outputGeometry[0]" "Cylinder_SRCShape.inMesh";
connectAttr "polyCylinder1.output" "Cylinder_SRCShapeOrig.inMesh";
connectAttr "joint1.scale" "joint2.inverseScale";
connectAttr "joint2.scale" "joint3.inverseScale";
connectAttr "joint3.scale" "joint4.inverseScale";
connectAttr "skinCluster2.outputGeometry[0]" "Cylinder_DSTShape.inMesh";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert1SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert1SG.message" ":defaultLightSet.message";
connectAttr "layerManager.displayLayerId[0]" "defaultLayer.identification";
connectAttr "renderLayerManager.renderLayerId[0]" "defaultRenderLayer.identification"
		;
connectAttr ":defaultArnoldDisplayDriver.message" ":defaultArnoldRenderOptions.drivers"
		 -nextAvailable;
connectAttr ":defaultArnoldFilter.message" ":defaultArnoldRenderOptions.filter";
connectAttr ":defaultArnoldDriver.message" ":defaultArnoldRenderOptions.driver";
connectAttr "Cylinder_SRCShapeOrig.worldMesh" "skinCluster1.input[0].inputGeometry"
		;
connectAttr "Cylinder_SRCShapeOrig.outMesh" "skinCluster1.originalGeometry[0]";
connectAttr "bindPose1.message" "skinCluster1.bindPose";
connectAttr "joint1.worldMatrix" "skinCluster1.matrix[0]";
connectAttr "joint2.worldMatrix" "skinCluster1.matrix[1]";
connectAttr "joint3.worldMatrix" "skinCluster1.matrix[2]";
connectAttr "joint1.lockInfluenceWeights" "skinCluster1.lockWeights[0]";
connectAttr "joint2.lockInfluenceWeights" "skinCluster1.lockWeights[1]";
connectAttr "joint3.lockInfluenceWeights" "skinCluster1.lockWeights[2]";
connectAttr "joint1.objectColorRGB" "skinCluster1.influenceColor[0]";
connectAttr "joint2.objectColorRGB" "skinCluster1.influenceColor[1]";
connectAttr "joint3.objectColorRGB" "skinCluster1.influenceColor[2]";
connectAttr "joint2.message" "skinCluster1.paintTrans";
connectAttr "ROOT.message" "bindPose1.members[0]";
connectAttr "JOINTS.message" "bindPose1.members[1]";
connectAttr "joint1.message" "bindPose1.members[2]";
connectAttr "joint2.message" "bindPose1.members[3]";
connectAttr "joint3.message" "bindPose1.members[4]";
connectAttr "bindPose1.world" "bindPose1.parents[0]";
connectAttr "bindPose1.members[0]" "bindPose1.parents[1]";
connectAttr "bindPose1.members[1]" "bindPose1.parents[2]";
connectAttr "bindPose1.members[2]" "bindPose1.parents[3]";
connectAttr "bindPose1.members[3]" "bindPose1.parents[4]";
connectAttr "joint1.bindPose" "bindPose1.worldMatrix[2]";
connectAttr "joint2.bindPose" "bindPose1.worldMatrix[3]";
connectAttr "joint3.bindPose" "bindPose1.worldMatrix[4]";
connectAttr "skinCluster1.outputGeometry[0]" "deltaMush1.input[0].inputGeometry"
		;
connectAttr "Cylinder_SRCShapeOrig.outMesh" "deltaMush1.originalGeometry[0]";
connectAttr ":initialShadingGroup.message" "MayaNodeEditorSavedTabsInfo.tabGraphInfo[0].nodeInfo[0].dependNode"
		;
connectAttr "Cylinder_DST.message" "MayaNodeEditorSavedTabsInfo.tabGraphInfo[0].nodeInfo[1].dependNode"
		;
connectAttr "Cylinder_DSTShape.message" "MayaNodeEditorSavedTabsInfo.tabGraphInfo[0].nodeInfo[2].dependNode"
		;
connectAttr "Cylinder_DSTShapeOrig.worldMesh" "skinCluster2.input[0].inputGeometry"
		;
connectAttr "Cylinder_DSTShapeOrig.outMesh" "skinCluster2.originalGeometry[0]";
connectAttr "joint1.worldMatrix" "skinCluster2.matrix[0]";
connectAttr "joint2.worldMatrix" "skinCluster2.matrix[1]";
connectAttr "joint3.worldMatrix" "skinCluster2.matrix[2]";
connectAttr "joint1.lockInfluenceWeights" "skinCluster2.lockWeights[0]";
connectAttr "joint2.lockInfluenceWeights" "skinCluster2.lockWeights[1]";
connectAttr "joint3.lockInfluenceWeights" "skinCluster2.lockWeights[2]";
connectAttr "joint1.objectColorRGB" "skinCluster2.influenceColor[0]";
connectAttr "joint2.objectColorRGB" "skinCluster2.influenceColor[1]";
connectAttr "joint3.objectColorRGB" "skinCluster2.influenceColor[2]";
connectAttr "bindPose1.message" "skinCluster2.bindPose";
connectAttr "joint2.message" "skinCluster2.paintTrans";
connectAttr ":lambert1.outColor" "lambert1SG.surfaceShader";
connectAttr "Cylinder_DSTShape.instObjGroups" "lambert1SG.dagSetMembers" -nextAvailable
		;
connectAttr "Cylinder_SRCShape.instObjGroups" "lambert1SG.dagSetMembers" -nextAvailable
		;
connectAttr "lambert1SG.message" "materialInfo1.shadingGroup";
connectAttr ":lambert1.message" "materialInfo1.material";
connectAttr "lambert1SG.message" "hyperShadePrimaryNodeEditorSavedTabsInfo.tabGraphInfo[0].nodeInfo[32].dependNode"
		;
connectAttr "lambert1SG.partition" ":renderPartition.sets" -nextAvailable;
connectAttr "defaultRenderLayer.message" ":defaultRenderingList1.rendering" -nextAvailable
		;
// End of CylinderTest.ma
