from typing import List

import numpy as np
from numpy.typing import NDArray


class Adam:
    def __init__(self, learning_rate: float = 0.001, beta1: float = 0.9, beta2: float = 0.999,
                 epsilon: float = 1e-8) -> None:

        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.first_moment_estimate = None
        self.second_moment_estimate = None
        self.iteration = 0

    def update(self, params: List[NDArray[np.float64]], grads: List[NDArray[np.float64]]) -> None:
        if self.first_moment_estimate is None:
            self.first_moment_estimate = [np.zeros_like(param) for param in params]
        if self.second_moment_estimate is None:
            self.second_moment_estimate = [np.zeros_like(param) for param in params]

        self.iteration += 1
        learning_rate_adjusted = self.learning_rate * (
                    np.sqrt(1 - self.beta2 ** self.iteration) / (1 - self.beta1 ** self.iteration))

        for i, (param, grad) in enumerate(zip(params, grads)):
            self.first_moment_estimate[i] = self.beta1 * self.first_moment_estimate[i] + (1 - self.beta1) * grad
            self.second_moment_estimate[i] = self.beta2 * self.second_moment_estimate[i] + (1 - self.beta2) * (
                        grad ** 2)

            first_moment_corrected = self.first_moment_estimate[i] / (1 - self.beta1 ** self.iteration)
            second_moment_corrected = self.second_moment_estimate[i] / (1 - self.beta2 ** self.iteration)

            param -= learning_rate_adjusted * first_moment_corrected / (np.sqrt(second_moment_corrected) + self.epsilon)
