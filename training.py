# coding=ascii
import json
import os
import numpy as np

import pandas

import tensorflow as tf
from tensorflow import keras
from tensorflow.contrib.keras.api.keras.layers import Dense
from tensorflow.contrib.keras.api.keras.models import Sequential

from fdda.logger import log
from fdda import constant as cst

_plot = True
try:
    import matplotlib.pyplot as plt
except Exception as e:
    log.debug(e)
    _plot = False


def read_inputs(directory: str) -> dict:
    """Read the input_data from the given directory"""
    input_file = os.path.normpath(os.path.join(directory, f"{cst.kInputName}.{cst.kExtension}"))
    with open(input_file) as f:
        return json.load(f)


def get_model(joints: np.array, verts: np.array, layers: int = 3,
              activation: str = 'tanh', units: int = 512, input_dim: int = 100):
    """!@Brief Build a training model based on the joint and vertices

    @param joints: Transformation matrix of the joint
    @param verts: Deltas of the vertices
    @param layers: The number of layers to create. A minimum of 2 is required.
    @param activation: The type of activation. Defaults to tanh
    @param units: The units per layer if not the input/output
    @param input_dim: The input dimensions of each layer that is not input/output
    @return: The model, name of the input node, the name of the output_node
    """
    model = Sequential()
    if layers < 2:
        log.warning("A minimum of 2 layers is required.")
        layers = 2

    input_name = 'input_node'
    output_name = 'output_node'
    for layer in range(layers):
        if not layer:
            model.add(Dense(units, input_dim=joints.shape[1], activation=activation, name=input_name))
            continue
        if layer == layers - 1:
            model.add(Dense(verts.shape[1], activation='linear', name=output_name))
            continue

        model.add(Dense(units, input_dim=input_dim, activation=activation, name="dense_layer_%s" % layer))

    output_node = model.output.name
    input_node = f"{input_name}_input:0"

    return model, input_node, output_node


def make_plot(history, output, show=True):
    """!@Brief Build a model from the trained keras model
    @param history: The output of the trained model
    @param output: Where to save the plot
    @param show: Whether to show the plot
    """
    plt.plot(history.history['mean_squared_error'])
    plt.plot(history.history['val_mean_squared_error'])
    plt.ylabel('mean_squared_error')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(output)
    if show:
        plt.show()

    return plt


def train(input_directory: str, rate: float = 0.001, epochs: float = 200, split: float = 0.01,
          batch_size: float = None, show: bool = True, activation: str = 'tanh',
          units: int = 512, input_dim: int = 100, layers: int = 3):
    """!@Brief Train the model from written data

    @param input_directory: The path to the directory where the data was written to
    @param rate: The learning rate. Lower rates are more accurate but slower.
    @param epochs: The number of epochs to train for.
                   Higher is more accurate but slower and there are diminishing returns.
    @param split: The training/testing split. Defaults to 0.3 for 70% training 30% test.
    @param batch_size: The batch size to train with.
    @param show: Show the plot after each model is done training.
    @param activation: What kind of activation to use. Defaults to tanh
    @param units: What units to use for intermediate layers.
    @param input_dim: Input dimensions to use for intermediate layers.
    @param layers: The number of layers to use. A minimum of 2 is enforced.
    @return: The path to the output json file
    """
    input_data = read_inputs(input_directory)
    csv_files = input_data.get('csv_files', list())
    joint_columns = input_data.get('input_fields', cst.kMatrixHeading)

    for i, csv_file in enumerate(csv_files):
        # Prepare the filesystem to write
        file_name, _ext = os.path.splitext(os.path.basename(csv_file))
        export_directory = os.path.join(input_directory, file_name)
        if not os.path.exists(export_directory):
            os.mkdir(export_directory)

        log.info(f"Training for {file_name}")
        # Read the csv of vert deltas to a pandas dataframe.
        df = pandas.read_csv(csv_file)
        df = df.drop_duplicates(joint_columns)
        if not df.shape[0] or df.shape[1] <= len(joint_columns):
            input_data.setdefault('models', list()).append(None)
            continue

        # Shuffle the data and split it into input and output data.
        df.reindex(np.random.permutation(df.index))
        joints = df.iloc[:, :len(joint_columns)]
        verts = df.iloc[:, len(joint_columns):]

        # Start making the model.
        with tf.Session(graph=tf.Graph()) as session:
            # Create a model.
            model, input_name, output_name = get_model(joints, verts, layers=layers, units=units,
                                                       input_dim=input_dim, activation=activation)

            # Generate the optimizer and train the model
            adam = keras.optimizers.Adam(lr=rate)
            model.compile(loss='mse', optimizer=adam, metrics=['mse'])
            history = model.fit(joints, verts, epochs=epochs, validation_split=split, batch_size=batch_size)

            # Show the plots
            plot_image = None
            if _plot:
                plot_image = os.path.join(export_directory, f"{file_name}.png")
                make_plot(history, plot_image, show=show)

            export_path = os.path.join(export_directory, file_name)

            # Save the keras model as a tensorflow model
            saver = tf.train.Saver(save_relative_paths=True)
            saver.save(session, export_path)

            # Store the data in a dict
            model_data = {'root': export_directory,
                          'meta': export_path + '.meta',
                          'input': input_name,
                          'output': output_name,
                          'plot': plot_image}

        # Then write this dict to the master dict
        input_data.setdefault('models', []).append(model_data)

    # Finally write this out to disk.
    output_data = os.path.join(input_directory, f"{cst.kOutputName}.{cst.kExtension}")
    with open(output_data, 'w') as f:
        json.dump(input_data, f, indent=cst.kJsonIndent)

    return output_data
