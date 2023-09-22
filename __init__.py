import os

_directory, _ = os.path.split(__file__)
poseDataDirectory = os.path.normpath(os.path.join(_directory, "posedata"))

kBipedLimitsPath = os.path.normpath(os.path.join(poseDataDirectory, "biped.json"))
