import numpy as np

from tensorflow.contrib.keras.api.keras.layers import Dense, LSTM, Conv2D, Flatten
from tensorflow.contrib.keras.api.keras.models import Sequential

from fdda.logger import log


class Activation(object):
    kRelu = "relu"
    kSigmoid = "sigmoid"
    kTanH = "tanh"
    kSoftmax = "softmax"
    kElu = "elu"
    kLinear = "linear"

    kDefault = kSigmoid


class Architecture(object):
    kDense = "dense"
    kRnn = "rnn"
    kCnn = "cnn"


class Settings(object):

    __kRateDefault = 0.001
    __kEpochsDefault = 200
    __kSplitDefault = 0.01
    __kBatchSizeDefault = None
    __kUnitsDefault = 512
    __kInputDimDefault = 100
    __kLayersDefault = 3
    __kArchitectureDefault = Architecture.kDense
    __kActivationDefault = Activation.kDefault
    __kActivationConv2DDefault = Activation.kRelu

    def __init__(self, **kwargs):
        """!@Brief Training settings

        @param architecture: Type of neuronal architecture used.
        @param input_directory: The path to the directory where the data was written to
        @param rate: The learning rate. Lower rates are more accurate but slower.
        @param epochs: The number of epochs to train for.
                       Higher is more accurate but slower and there are diminishing returns.
        @param split: The training/testing split. Defaults to 0.3 for 70% training 30% test.
        @param batch_size: The batch size to train with.
        @param show: Show the plot after each model is done training.
        @param activation: What kind of activation to use. Defaults to sigmoid
        @param units: What units to use for intermediate layers.
        @param input_dim: Input dimensions to use for intermediate layers.
        @param layers: The number of layers to use. A minimum of 2 is enforced.
        """
        self.rate = kwargs.get("rate", self.__kRateDefault)
        self.epochs = kwargs.get("epochs", self.__kEpochsDefault)
        self.split = kwargs.get("split", self.__kSplitDefault)
        self.batch_size = kwargs.get("batch_size", self.__kBatchSizeDefault)
        self.units = kwargs.get("units", self.__kUnitsDefault)
        self.input_dim = kwargs.get("input_dim", self.__kInputDimDefault)
        self.layers = kwargs.get("layers", self.__kLayersDefault)
        self.architecture = kwargs.get("architecture", self.__kArchitectureDefault)
        self.activation = kwargs.get("activation", self.__kActivationDefault)
        self.activation_conv = kwargs.get("activation_conv", self.__kActivationConv2DDefault)

    @classmethod
    def default(cls):
        return cls()


def _get_model_mlp(settings: Settings, joints: np.array, verts: np.array) -> tuple:
    model = Sequential()
    if settings.layers < 2:
        log.warning("A minimum of 2 layers is required.")
        settings.layers = 2

    input_name = 'input_node'
    output_name = 'output_node'
    for layer in range(settings.layers):
        if not layer:
            model.add(Dense(settings.units, input_dim=joints.shape[1],
                            activation=settings.activation, name=input_name))
            continue
        if layer == settings.layers - 1:
            model.add(Dense(verts.shape[1], activation='linear', name=output_name))
            continue

        model.add(Dense(settings.units, input_dim=settings.input_dim,
                        activation=settings.activation, name=f"dense_layer_{layer}"))

    output_node = model.output.name
    input_node = f"{input_name}_input:0"

    return model, input_node, output_node


def _get_model_rnn(settings: Settings, joints: np.array, verts: np.array) -> Sequential:
    """Build a training model based on the joint and vertices with an RNN architecture (LSTM)"""
    model = Sequential()
    model.add(LSTM(settings.units, input_shape=(None, joints.shape[1])))
    model.add(Dense(verts.shape[1], activation=settings.activation))

    return model


def _get_model_cnn(settings: Settings, joints: np.array, verts: np.array) -> Sequential:
    """Build a training model based on the joint and vertices with a CNN architecture"""
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation=settings.activation_conv,
                     input_shape=(joints.shape[1], joints.shape[2], 1)))
    model.add(Flatten())
    model.add(Dense(verts.shape[1], activation=settings.activation))

    return model


_kMapping = {Architecture.kDense: _get_model_mlp,
             Architecture.kRnn: _get_model_rnn,
             Architecture.kCnn: _get_model_cnn}


def get_model(settings: Settings, joints, verts):
    if settings.architecture not in _kMapping:
        raise RuntimeError(f"Unknown architecture given: {settings.architecture} !")
    return _kMapping[settings.architecture](settings, joints, verts)
