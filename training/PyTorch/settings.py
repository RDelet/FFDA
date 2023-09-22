from textwrap import dedent

from torch import cuda as cuda
from torch import nn as nn

from fdda.core.logger import log


class Activation:

    kRelu = nn.ReLU()
    kSigmoid = nn.Sigmoid()
    kTanH = nn.Tanh()
    kSoftmax = nn.Softmax()
    kElu = nn.ELU()
    kLeakyRelu = nn.LeakyReLU()
    kLinear = "linear"

    kDefault = kTanH


class Architecture:
    kDense = "dense"


class Settings:

    kRate = "rate"  # The learning rate. Lower rates are more accurate but slower.
    kEpochs = "epochs"  # The number of epochs to train for.
    kSplit = "split"  # The training/testing split. Defaults to 0.3 for 70% training 30% test.
    kBatchSize = "batch_size"  # The batch size to train with. If unspecified, batch_size will
    kUnits = "units"  # What units to use for intermediate layers.
    kInputDim = "input_dim"  # Input dimensions to use for intermediate layers.
    kLayers = "layers"  # The number of layers to use. A minimum of 2 is enforced.
    kArchitecture = "architecture"  # Type of neuronal architecture used.
    kActivation = "activation"  # What kind of activation to use. Defaults to tanh
    kShuffle = "shuffle"  # Enable/Disable the random shuffling of data.
    kEarlyStop = "early_stop"  # The number of consecutive iterations in which the loss function no
    kDevice = "device"  # GPU or CPU.

    kCpu = "cpu"
    kGpu = "gpu"

    __kRateDefault = 1e-3
    __kEpochsDefault = 800
    __kSplitDefault = 0.3
    __kBatchSizeDefault = 32
    __kShuffle = True
    __kUnitsDefault = 512
    __kInputDimDefault = 100
    __kLayersDefault = 4
    __kEarlyStop = 20
    __kArchitectureDefault = Architecture.kDense
    __kActivationDefault = Activation.kElu
    __kDevice = kCpu

    def __init__(self, **kwargs):
        self.rate = kwargs.get(self.kRate, self.__kRateDefault)
        self.epochs = kwargs.get(self.kEpochs, self.__kEpochsDefault)
        self.split = kwargs.get(self.kSplit, self.__kSplitDefault)
        self.batch_size = kwargs.get(self.kBatchSize, self.__kBatchSizeDefault)
        self.units = kwargs.get(self.kUnits, self.__kUnitsDefault)
        self.input_dim = kwargs.get(self.kInputDim, self.__kInputDimDefault)
        self.layers = kwargs.get(self.kLayers, self.__kLayersDefault)
        self.architecture = kwargs.get(self.kArchitecture, self.__kArchitectureDefault)
        self.activation = kwargs.get(self.kActivation, self.__kActivationDefault)
        self.shuffle = kwargs.get(self.kShuffle, self.__kShuffle)
        self.early_stop = kwargs.get(self.kEarlyStop, self.__kEarlyStop)
        self.device = kwargs.get(self.kDevice, self.__kDevice)

        if not(cuda.is_available()):
            self.device = self.kCpu

    def __str__(self):
        msg = dedent(
            f"""
            The model is train with:
                Learning rate: {self.rate}
                Batch size: {self.batch_size}
                Number of epochs: {self.epochs}
            """
        )
        log.info(msg)

    @classmethod
    def default(cls):
        return cls()
