# coding=ascii

import json
import numpy as np
import os
import traceback

from torch import cuda, load as torch_load

from fdda.core import constant
from fdda.core.logger import log
from fdda.training.PyTorch.architecture import MultiLayerPerceptron, TorchModel


class Loader:

    def __init__(self):

        self._models = []
        self._means = []
        self._stds = []

        self._file_path = None
        self._device = constant.kCPU
        self._normalized = False
        self._global_mode = False
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"FDDA(class: {self.__class__.__name__}, filePath: {self._file_path})"
    
    def clear(self):

        self._models = []
        self._means = []
        self._stds = []

        self._file_path = None
        self._device = constant.kCPU
        self._normalized = False
        self._global_mode = False
    
    @property
    def models(self) -> list:
        return self._models
    
    @property
    def model_count(self) -> int:
        return len(self._models)
    
    @property
    def means(self) -> list:
        return self._means
    
    @property
    def stds(self) -> list:
        return self._stds
    
    @property
    def device(self) -> str:
        return self._device

    @property
    def normalized(self) -> bool:
        return self._normalized
    
    @property
    def file(self) -> str:
        return self._file_path
    
    def global_mode(self) -> bool:
        return self._global_mode

    def _load(self, data: dict):
        self._device = self._get_device(data)
        self._normalized = data.get(constant.kNormalized, False)
        self._global_mode = data.get(constant.kMode, False)

        for i, model_data in enumerate(data[constant.kModels]):
            model = None
            mean = None
            std = None

            if model_data:
                mean = model_data.get(constant.kMean)
                std = model_data.get(constant.kStd)
                if not mean or not std:
                    raise RuntimeError("Error on get model data !")
                model = self._deserialize(i, data, model_data)

            self._models.append(model)
            self._means.append(mean)
            self._stds.append(std)

    def load(self, file_path: str) -> bool:
        """!@Brief Load models from the json file given."""

        self.clear()
        data = self._read(file_path)
        if constant.kModels not in data:
            log.error(f"No models found !")
            return

        try:
            self._load(data)
        except Exception as e:
            log.error(e)
            log.debug(traceback.format_exc())
            self.clear()
            return False
        
        return True
    
    def _get_device(self, data: dict):
        device = constant.kCPU
        if cuda.is_available() and data[self.kDevice] == "gpu":
            device = constant.kGPU

        return device
    
    def _read(self, file_path: str) -> dict:

        data = {}
        if not os.path.exists(file_path):
            log.error(f"Could not find file {file_path} !")
            return data

        self._file_path = file_path
        try:
            log.info(f"Loading models from {file_path}")
            with open(self._file_path, "r") as f:
                data = json.load(f)
        except Exception as e:
            log.error(e)
            log.debug(traceback.format_exc)
            self.clear()
        
        return data

    def _deserialize(self, model_ids: int, data: dict, model: dict) -> TorchModel:
        if self._global_mode:
            vertices = np.concatenate(data[constant.kJointMap], dtype=np.float32)
            vertices = vertices.astype(np.int32)
        else:
            vertices = data[constant.kJointMap][model_ids]

        checkpoint = torch_load(model[constant.kBestModel])
        model = MultiLayerPerceptron(settings=checkpoint['settings'],
                                     input_shape=checkpoint['input_shape'],
                                     output_shape=checkpoint['output_shape'])
        model.to(self._device)
        model.load_state_dict(checkpoint['model_state_dict'])

        return TorchModel(model=model, vertices=vertices)