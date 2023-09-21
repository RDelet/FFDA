import numpy as np

EPSILON = np.finfo(np.float32).eps

def feature_standardization(features, mean, std):
    """ !@Brief Normalize features by given mean and standard deviation."""
    return (features - mean) / (std + EPSILON)
