# coding=ascii
import os
import csv
from time import time
from datetime import datetime
import json
import random

import numpy as np
import pandas as pd
import torch
from torch import nn as nn
from torchinfo import summary
from torch.utils.tensorboard import SummaryWriter

from fdda.core.logger import log
from fdda.core import constant as cst
from fdda.training.PyTorch.architecture import MultiLayerPerceptron, Activation, Settings, fit
from fdda.training.PyTorch.dataset import FDDADataset
from fdda.training.PyTorch.math import feature_standardization


_plot = False
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


def make_plot(history, output, legend=None, show=True):
    """!@Brief Build a model from the trained keras model
        @param history: The output of the trained model
        @param output: Where to save the plot
        @param legend: Name of each traced curve
        @param show: Whether to show the plot
    """
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.ylabel('mean_squared_error')
    plt.xlabel('epoch')
    if legend is not None:
        plt.legend(legend, loc='upper left')
    plt.savefig(output)
    if show:
        plt.show()
    return plt


def merge_data(input_data: dict) -> tuple:
    csv_files = input_data.get('csv_files', list())
    joint_columns = input_data.get('input_fields', cst.kInputHeading)
    joints_ids = input_data.get("joint_indexes", list())
    joint_map = input_data.get("joint_map", list())
    input_len = len(joint_columns)

    in_data = []
    delta_data = []
    input_header = []
    output_header = []

    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(csv_file)
        n_coord = len(joint_map[i]) * 3

        if i == 0:
            in_data = df.iloc[:, :input_len].values
            delta_data = df.iloc[:, input_len:n_coord+input_len].values
        else:
            in_data = np.concatenate((in_data, df.iloc[:, :input_len].values), axis=1)
            delta_data = np.concatenate((delta_data, df.iloc[:, input_len:n_coord+input_len].values), axis=1)

        input_header.extend([f"q{joints_ids[i]}x", f"q{joints_ids[i]}y", f"q{joints_ids[i]}z", f"q{joints_ids[i]}w"])
        output_header.extend(list(df.columns[input_len:]))

        log.info(f"Merge data from {csv_file}")

    data = np.concatenate((in_data, delta_data), axis=1)
    heading = input_header + output_header
    input_len = len(input_header)
    joint_columns = input_header

    # clear memory
    del in_data
    del delta_data

    out_dir = os.path.split(csv_file)[0]
    file_path = os.path.join(out_dir, "GlobalJoints.csv")

    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(heading)
        writer.writerows(data.tolist())

    csv_files = [file_path]

    return csv_files, input_len, joint_columns


def build_models(input_directory: str,
                 settings: Settings = Settings.default(), mode: bool = False, normalized: bool = False,
                 debug: bool = False):
    """
        !@Brief Build all the models from the 3d mesh and network parameters.

        @param input_directory: str, the path where the deep learning model will be saved
        @param settings: Settings, the network parameters.
        @param normalized: bool, if True, apply normalization on the data.
        @param debug: bool, if True the results will be reproducible.
        @param mode: bool, if True the bone rotations and associated vertices are saved in
            the same file. This mode is used to train a global model which learns
            delta for all vertices in a mesh.
    """

    # GPU configuration.
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.deterministic = False
    torch.backends.cudnn.enabled = True

    # To obtain reproducible results
    if debug:
        torch.backends.cudnn.benchmark = True
        random.seed(1)
        np.random.seed(1)
        torch.manual_seed(1)
        torch.cuda.manual_seed(1)

    # Take data stored from the input .json file
    input_data = read_inputs(input_directory)
    csv_files = input_data.get('csv_files', list())
    joint_columns = input_data.get('input_fields', cst.kInputHeading)
    input_length = len(joint_columns)
    n_coordinates = input_data.get('n_vertices', int) * 3

    start = time()

    if mode:
        csv_files, input_length, joint_columns = merge_data(input_data)
        input_data['input_length'] = input_length
        input_data['csv_files'] = csv_files

    for i, csv_file in enumerate(csv_files):

        # Prepare the filesystem to write
        file_name, _ext = os.path.splitext(os.path.basename(csv_file))
        export_directory = os.path.join(input_directory, file_name)
        if not os.path.exists(export_directory):
            os.mkdir(export_directory)

        # Read the csv of vert deltas to a pandas dataframe.
        df = pd.read_csv(csv_file)
        df = df.drop_duplicates(joint_columns)
        if not df.shape[0] or df.shape[1] <= input_length:
            input_data.setdefault('models', list()).append(None)
            continue

        # Check if the training set can be splitted.
        if (df.shape[0] * settings.split < 1.) and settings.split > 0.:
            input_data.setdefault('models', list()).append(None)
            continue

        # Split data into input and output data.
        data = {}
        data['joints'] = df.iloc[:, :input_length].values.astype(np.float32)
        data['delta'] = df.iloc[:, input_length:(n_coordinates+input_length)].values.astype(np.float32)

        # Compute statistics
        mean = np.mean(data['joints'], axis=0)
        std = np.std(data['joints'], axis=0)
        
        if normalized:
            data['joints'] = feature_standardization(data['joints'], mean, std)

        # Prepare data
        log.info(f"Training for {file_name}")

        # Split data into trainset and validset
        # L'avantage de la validation est de valider le modele sur un ensemble non appris.
        # Ce qui permet de visualiser la capacite du modele a generaliser.
        if settings.split > 0.:
            shuffle_ids = list(range(0, data['joints'].shape[0]))
            random.shuffle(shuffle_ids)
            validation_length = int(data['joints'].shape[0] * settings.split)
            validation_ids = shuffle_ids[:validation_length]
            train_ids = shuffle_ids[validation_length:]
            valid_set = FDDADataset({'joints': data['joints'][validation_ids, :],
                                     'delta': data['delta'][validation_ids, :]}
                                    )
            valid_loader = torch.utils.data.DataLoader(
                valid_set,
                batch_size=settings.batch_size,
                shuffle=False,
                num_workers=0,
                prefetch_factor=2,
                pin_memory=True)
        else:
            valid_loader = None
            train_ids = range(0, data['joints'].shape[0])

        train_set = FDDADataset({'joints': data['joints'][train_ids, :],
                                 'delta': data['delta'][train_ids, :]}
                                )
        train_loader = torch.utils.data.DataLoader(
            train_set,
            batch_size=settings.batch_size,
            shuffle=settings.shuffle,
            num_workers=0,
            prefetch_factor=2,
            pin_memory=True)

        # Tensorboard writer
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        writer = SummaryWriter(log_dir=os.path.join(export_directory, 'tensorboard_{}'.format(timestamp)))

        # Instantiate network
        net = MultiLayerPerceptron(settings,
                                   input_shape=train_set.joints.shape,
                                   output_shape=train_set.delta.shape)

        optimizer = torch.optim.Adam(net.parameters(), lr=settings.rate)
        criterion = nn.MSELoss(reduction='mean')

        # If running on GPU
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        if torch.cuda.is_available():
            net = net.cuda()

        # Display network configuration like Keras's summary
        input_size = (settings.batch_size, train_set.joints.shape[1])
        log.info(summary(net, input_size=input_size))

        # Train network
        history, opti_model_state_file = fit(model=net,
                                             train_loader=train_loader,
                                             validation_loader=valid_loader,
                                             loss_func=criterion,
                                             optimizer=optimizer,
                                             writer=writer,
                                             save_dir=export_directory,
                                             settings=settings,
                                             input_shape=train_set.joints.shape,
                                             output_shape=train_set.delta.shape,
                                             epochs=settings.epochs,
                                             batch_size=settings.batch_size,
                                             device=device)

        writer.close()

        # Show the plots
        plot_image = None
        if _plot:
            plot_image = os.path.join(export_directory, f"{file_name}.png")
            curr_jnt = 'jnt_' + str(i + 1)
            legend = ['train_' + curr_jnt, 'valid_' + curr_jnt]
            make_plot(history, plot_image, legend=legend, show=debug)

        # Save the final model as pytorch model
        model_state_file = os.path.join(export_directory, 'final_ckpt.pt')
        torch.save({'model_state_dict': net.state_dict(),
                    'input_shape': train_set.joints.shape,
                    'output_shape': train_set.delta.shape,
                    'settings': settings}, model_state_file)

        # Store the data in a dict
        model_data = {'root': export_directory,
                      'model': model_state_file,
                      'best_model': opti_model_state_file,
                      'plot': plot_image,
                      'mean': mean.tolist(),
                      'std': std.tolist()}

        # Then write this dict to the master dict
        input_data.setdefault('models', []).append(model_data)

    elapsed_training_time = time() - start
    log.info("Finished... Done in {}h {}min, {}s".format(int(elapsed_training_time / 3600),
                                                         int((elapsed_training_time % 3600) / 60),
                                                         int((elapsed_training_time % 3600) % 60)))

    # Add the device used during the training
    input_data.setdefault('device', settings.device)

    input_data.setdefault('normalized', normalized)
    input_data.setdefault('global_mode', mode)


    # Finally write this out to disk.
    output_data = os.path.join(input_directory, f"{cst.kOutputName}.{cst.kExtension}")
    with open(output_data, 'w') as f:
        json.dump(input_data, f, indent=cst.kJsonIndent)

    return output_data


"""
if __name__ == '__main__':
    settings = Settings.default()
    settings.rate = 1e-3
    settings.layers = 4
    settings.epochs = 800
    settings.activation = Activation.kElu
    settings.split = 0.1
    settings.units = 256
    settings.batch_size = 128
    settings.device = 'gpu'

    build_models(input_directory=f"D:\Documents\Machine_Learning_Projects\MLDeformer\Scenes\Dana_fdda_low_without_muslce",
                 settings=settings, mode=True, normalized=True, debug=True)
"""