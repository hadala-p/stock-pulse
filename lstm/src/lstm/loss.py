import numpy as np


class MeanSquaredError:
    def forward(self, predicted, actual):
        return np.mean((predicted - actual) ** 2)

    def backward(self, predicted, actual):
        return 2 * (predicted - actual) / actual.size


class CrossEntropyLoss:
    def forward(self, predicted, actual):
        epsilon = 1e-12
        predicted = np.clip(predicted, epsilon, 1. - epsilon)
        return -np.sum(actual * np.log(predicted)) / predicted.shape[0]

    def backward(self, predicted, actual):
        epsilon = 1e-12
        predicted = np.clip(predicted, epsilon, 1. - epsilon)
        return -(actual / predicted) / actual.shape[0]
