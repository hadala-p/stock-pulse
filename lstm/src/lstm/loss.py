import numpy as np
from numpy.typing import NDArray


class MeanSquaredError:
    @staticmethod
    def forward(predicted: NDArray[np.float64], actual: NDArray[np.float64]) -> np.floating:
        return np.mean((predicted - actual) ** 2)

    @staticmethod
    def backward(predicted: NDArray[np.float64], actual: NDArray[np.float64]) -> NDArray[np.float64]:
        return 2 * (predicted - actual) / actual.size


class CrossEntropyLoss:
    @staticmethod
    def forward(predicted: NDArray[np.float64], actual: NDArray[np.float64]) -> float:
        epsilon: float = 1e-12
        predicted = np.clip(predicted, epsilon, 1. - epsilon)
        return -np.sum(actual * np.log(predicted)) / predicted.shape[0]

    @staticmethod
    def backward(predicted: NDArray[np.float64], actual: NDArray[np.float64]) -> NDArray[np.float64]:
        epsilon: float = 1e-12
        predicted = np.clip(predicted, epsilon, 1. - epsilon)
        return -(actual / predicted) / actual.shape[0]
