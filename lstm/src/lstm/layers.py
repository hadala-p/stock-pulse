from typing import Tuple

import numpy as np
from numpy.typing import NDArray


class LSTMLayer:
    def __init__(self, input_size: int, hidden_size: int) -> None:
        self.input_size = input_size
        self.hidden_size = hidden_size

        self.forget_gate_weights: NDArray[np.float64] = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.forget_gate_bias: NDArray[np.float64] = np.zeros((hidden_size, 1))

        self.input_gate_weights: NDArray[np.float64] = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.input_gate_bias: NDArray[np.float64] = np.zeros((hidden_size, 1))

        self.output_gate_weights: NDArray[np.float64] = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.output_gate_bias: NDArray[np.float64] = np.zeros((hidden_size, 1))

        self.cell_state_weights: NDArray[np.float64] = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.cell_state_bias: NDArray[np.float64] = np.zeros((hidden_size, 1))

    @staticmethod
    def sigmoid(x: NDArray[np.float64]) -> NDArray[np.float64]:
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def tanh(x: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.tanh(x)

    def forward(self,
                x: NDArray[np.float64],
                previous_hidden_state: NDArray[np.float64],
                previous_cell_state: NDArray[np.float64]
                ) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        # Concatenate previous hidden state and input
        concatenated_input: NDArray[np.float64] = np.vstack((previous_hidden_state, x))

        forget_gate_output: NDArray[np.float64] = self.sigmoid(
            np.dot(self.forget_gate_weights, concatenated_input) + self.forget_gate_bias)

        input_gate_output: NDArray[np.float64] = self.sigmoid(
            np.dot(self.input_gate_weights, concatenated_input) + self.input_gate_bias)

        output_gate_output: NDArray[np.float64] = self.sigmoid(
            np.dot(self.output_gate_weights, concatenated_input) + self.output_gate_bias)

        candidate_cell_state: NDArray[np.float64] = self.tanh(
            np.dot(self.cell_state_weights, concatenated_input) + self.cell_state_bias)
        updated_cell_state: NDArray[
            np.float64] = forget_gate_output * previous_cell_state + input_gate_output * candidate_cell_state

        updated_hidden_state: NDArray[np.float64] = output_gate_output * self.tanh(updated_cell_state)

        return updated_hidden_state, updated_cell_state
