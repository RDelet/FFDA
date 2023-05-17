# coding=ascii
import json
import os
import numpy as np

import pandas

import tensorflow as tf
from tensorflow import keras

from fdda.logger import log
from fdda import constant as cst
from fdda.architecture import Architecture, get_model, Settings

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


def train(input_directory: str, settings: Settings, show: bool = True) -> str:
    """!@Brief Train the model from written data

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

        # Start making the model
        with tf.Session(graph=tf.Graph()) as session:
            model, input_name, output_name = __get_model(joints, verts, settings)

            # Generate the optimizer and train the model
            adam = keras.optimizers.Adam(lr=settings.rate)
            model.compile(loss='mse', optimizer=adam, metrics=['mse'])
            history = model.fit(joints, verts, epochs=settings.epochs,
                                validation_split=settings.split,
                                batch_size=settings.batch_size)

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


def __get_model(joints, verts, settings):
    model_data = get_model(settings, joints, verts)
    model = model_data[0]
    input_name = model_data[1] if settings.architecture == Architecture.kDense else None
    output_name = model_data[2] if settings.architecture == Architecture.kDense else None

    return model, input_name, output_name
