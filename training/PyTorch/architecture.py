import os
from collections import namedtuple
from time import time
from tqdm import tqdm

import numpy as np
from torch import inf as torchInf, no_grad, save as torchSave, from_numpy
from torch.nn import Module, Linear, Sequential

from fdda.core.logger import log
from fdda.training.PyTorch.callbacks import EarlyStop
from fdda.training.PyTorch.math import feature_standardization
from fdda.training.PyTorch.settings import Settings, Activation


TorchModel = namedtuple("TorchModel", ["model", "vertices"])


class MultiLayerPerceptron(Module):

    def __init__(self,
                 settings: Settings,
                 input_shape: np.array,
                 output_shape: np.array,
                 **kwargs):
        """!@Brief This class implements a vertex delta model that learns how to correct
                   the deformation error in a mesh by learning a list of delta from the
                   rotation of all bone rotation.
        """
        super().__init__()

        layers = []
        if settings.layers < 2:
            log.warning("A minimum of 2 layers is required.")
            settings.layers = 2

        for layer in range(settings.layers):
            if not layer:
                layers.append(Linear(in_features=input_shape[1], out_features=settings.units))
                if settings.activation is not Activation.kLinear:
                    layers.append(settings.activation)
                continue
            # Last layer should have a linear activation function.
            if layer == settings.layers - 1:
                layers.append(Linear(in_features=settings.units, out_features=output_shape[1]))
                continue

            layers.append(Linear(in_features=settings.units, out_features=settings.units))
            if settings.activation is not Activation.kLinear:
                layers.append(settings.activation)

        self.net = Sequential(*layers)
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"FDDA(class: {self.__class__.__name__}, module: Pytorch)"

    def forward(self, inputs):
        return self.net(inputs)


# Training function
def fit(model, train_loader, validation_loader, loss_func, optimizer, writer, save_dir, settings,
        input_shape, output_shape, epochs, batch_size=32, device='cpu'):
    """!@Brief Train function.

        @param model: The network to be trained.
        @param train_loader: The training set.
        @param validation_loader: The validation set.
        @param loss_func: The cost function.
        @param optimizer: The optimizer function.
        @param writer: Tensorboard writer.
        @param save_dir: directory where the model checkpoint will be saved.
        @param settings: parameters of the training.
        @param input_shape: input dimensions.
        @param output_shape: output dimensions.
        @param epochs: Number of training epochs.
        @param batch_size: Number of samples per batch.
        @param device: Device, by default the training run on cpu.
    """
    log.info("train() called: model=%s, opt=%s(lr=%f), epochs=%d, batch_size=%d, device=%s\n" %
             (type(model).__name__, type(optimizer).__name__, optimizer.param_groups[0]['lr'],
             epochs, batch_size, device))

    # Collects per-epoch loss and acc like Keras' fit().
    history = {}
    history['loss'] = []
    history['val_loss'] = []

    callback = EarlyStop(patience=20)

    model_state_file = os.path.join(save_dir, 'optimal_ckpt.pt')

    for epoch in range(0, epochs):

        # Time measures.
        loading_time = 0.0
        processing_time = 0.0

        # Global epoch loss.
        epoch_loss = 0.0
        n_samples = 0

        # Make sure the model run in training mode.
        model.train()
        start = time()

        with tqdm(enumerate(train_loader), unit='batch', miniters=2) as pbar:
            for i, (joints, delta_true) in pbar:
                pbar.set_description(f"Epoch [{epoch}/{epochs}]")
                joints, delta_true = joints.to(device), delta_true.to(device)
                # Measure loading data process time to find any bottleneck.
                tmp_load_timer = (time() - start)
                loading_time += tmp_load_timer
                # Clear the gradients
                optimizer.zero_grad()
                # Forward Pass: Compute predictions.
                delta = model(joints)
                # Compute loss.
                loss = loss_func(delta, delta_true)
                # Backpropagation.
                loss.backward()
                optimizer.step()
                # Average loss along the dataset.
                n_samples += joints.size(0)
                epoch_loss += loss.item() * joints.size(0)
                # Measure processing time.
                processing_time += time() - (start + tmp_load_timer)
                # Logs
                pbar.set_postfix(loss=(epoch_loss / n_samples), computation_time=(processing_time / n_samples),
                                 loading_time=(loading_time / n_samples))

                start = time()

        # Validation step
        if validation_loader is not None:
            model.eval()

            val_samples = 0
            v_loss = 0.0

            # Disable gradient computation and reduce memory consumption.
            with no_grad():
                for i, (joints, delta_true) in enumerate(validation_loader):
                    joints, delta_true = joints.to(device), delta_true.to(device)

                    # Forward Pass: Compute predictions.
                    delta = model(joints)

                    # Compute loss.
                    loss = loss_func(delta, delta_true)

                    # Average loss along the dataset.
                    val_samples += joints.size(0)
                    v_loss += loss.item() * joints.size(0)

            writer.add_scalar('Loss/validation', (v_loss / val_samples), epoch)
            history['val_loss'].append((v_loss / val_samples))

        # Update Tensorboard.
        writer.add_scalar('Loss/train', (epoch_loss / n_samples), epoch)

        # Update history.
        history['loss'].append((epoch_loss / n_samples))

        # Save the best learned model.
        is_best = (v_loss / val_samples) < torchInf

        if is_best:
            torchSave({'model_state_dict': model.state_dict(),
                       'input_shape': input_shape,
                       'output_shape': output_shape,
                       'settings': settings}, model_state_file)

        if callback.early_stop((epoch_loss / n_samples)):
            log.info('=> '.format(save_dir))
            break

    writer.flush()
    return history, model_state_file


# Evaluation function
def evaluation(model, inputs, loss_func, batch_size=32, device='cpu'):
    pass


def get_prediction(model: TorchModel, inputs: np.array,
                   mean: list, std: list,
                   normalized: bool = True, device: str = "cpu") -> np.array:
        # Apply normalization
        if normalized:
            mean = np.array(mean, dtype=np.float32)
            std = np.array(std, dtype=np.float32)
            inputs = feature_standardization(inputs, mean, std)
        # Convert Numpy -> torch.Tensor
        inputs = from_numpy(inputs).to(device)
        # Prediction
        prediction = model.model(inputs)
        # Convert torch.Tensor -> Numpy
        prediction = prediction.detach().cpu().numpy()

        return prediction
