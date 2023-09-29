#ifndef MULTI_LAYER_PERCEPTRON_H
#define MULTI_LAYER_PERCEPTRON_H

#include "common.h"
#include "settings.h"


class MultiLayerPerceptron : torch::nn::Module {

	public:
		MultiLayerPerceptron();
		MultiLayerPerceptron(Settings& _settings, MPointArray& _inputShape, MPointArray& _outputShape) {

			std::vector<torch::nn::Linear> layers;
			if (_settings.layers < 2) {
				MGlobal::displayWarning("A minimum of 2 layers is required.");
				_settings.layers = 2;
			}

			for (int i = 0; i < _settings.layers; i++) {
				if (layers.size() == 0) {
					torch::nn::Linear pouet = torch::nn::Linear(_inputShape[0], _settings.units);
					layers.push_back(pouet);
					/*
					if (_settings.activation == kLinear) {
						layers.push_back(_settings.activation);
					}
					*/
					continue;
				}

				if (layers.size() == _settings.layers - 1) {
					torch::nn::Linear groot = torch::nn::Linear(_settings.units, _outputShape[0]);
					layers.push_back(groot);
					continue;
				}

				torch::nn::Linear kapouet = torch::nn::Linear(_settings.units, _settings.units);
				layers.push_back(kapouet);
				/*
				if (_settings.activation == kLinear) {
					layers.push_back(_settings.activation);
				}
				*/
			}

			net = torch::nn::Sequential(layers);

		}
		virtual					~MultiLayerPerceptron() {}

		void					forward(torch::Tensor& x) { net(x); }

	public:

		torch::nn::Sequential	net;

};


struct TorchModel {

	MultiLayerPerceptron	model = MultiLayerPerceptron();
	std::vector<int>		vertices = std::vector<int>();

};


#endif