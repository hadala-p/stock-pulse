import numpy as np
from numpy.typing import NDArray


def sigmoid(x: NDArray[np.float64]) -> NDArray[np.float64]:
    return 1 / (1 + np.exp(-x))


def tanh(x: NDArray[np.float64]) -> NDArray[np.float64]:
    return np.tanh(x)


def relu(x: NDArray[np.float64]) -> NDArray[np.float64]:
    return np.maximum(0, x)
