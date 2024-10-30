from typing import Tuple
import numpy as np
from numpy.typing import NDArray
from lstm.activations import sigmoid, tanh


class LSTMLayer:
    def __init__(self, input_size: int, hidden_size: int, dropout_rate: float = 0.0) -> None:
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.dropout_rate = dropout_rate

        # Weights and biases for gates
        self.forget_gate_weights = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.forget_gate_bias = np.zeros((hidden_size, 1))
        self.input_gate_weights = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.input_gate_bias = np.zeros((hidden_size, 1))
        self.output_gate_weights = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.output_gate_bias = np.zeros((hidden_size, 1))
        self.cell_state_weights = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.cell_state_bias = np.zeros((hidden_size, 1))

        self.cache = []

    def forward(self, x: NDArray[np.float64], previous_hidden_state: NDArray[np.float64], previous_cell_state: NDArray[np.float64]) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        concatenated_input = np.vstack((previous_hidden_state, x))

        forget_gate_output = sigmoid(np.dot(self.forget_gate_weights, concatenated_input) + self.forget_gate_bias)
        input_gate_output = sigmoid(np.dot(self.input_gate_weights, concatenated_input) + self.input_gate_bias)
        output_gate_output = sigmoid(np.dot(self.output_gate_weights, concatenated_input) + self.output_gate_bias)
        candidate_cell_state = tanh(np.dot(self.cell_state_weights, concatenated_input) + self.cell_state_bias)

        updated_cell_state = forget_gate_output * previous_cell_state + input_gate_output * candidate_cell_state
        updated_hidden_state = output_gate_output * tanh(updated_cell_state)

        if self.dropout_rate > 0:
            dropout_mask = (np.random.rand(*updated_hidden_state.shape) > self.dropout_rate).astype(float)
            updated_hidden_state *= dropout_mask / (1 - self.dropout_rate)

        self.cache.append((concatenated_input, forget_gate_output, input_gate_output, output_gate_output, candidate_cell_state, updated_cell_state, previous_cell_state, previous_hidden_state))
        return updated_hidden_state, updated_cell_state

    def backward(self, next_hidden_state_gradient: np.ndarray, next_cell_state_gradient: np.ndarray):
        # Initialize gradients
        gradient_forget_gate_weights = np.zeros_like(self.forget_gate_weights)
        gradient_forget_gate_bias = np.zeros_like(self.forget_gate_bias)
        gradient_input_gate_weights = np.zeros_like(self.input_gate_weights)
        gradient_input_gate_bias = np.zeros_like(self.input_gate_bias)
        gradient_output_gate_weights = np.zeros_like(self.output_gate_weights)
        gradient_output_gate_bias = np.zeros_like(self.output_gate_bias)
        gradient_cell_state_weights = np.zeros_like(self.cell_state_weights)
        gradient_cell_state_bias = np.zeros_like(self.cell_state_bias)

        # Initialize gradients for inputs
        previous_hidden_gradient = np.zeros_like(next_hidden_state_gradient)
        previous_cell_gradient = np.zeros_like(next_cell_state_gradient)

        for t in reversed(range(len(self.cache))):
            (
            concatenated_input, forget_output, input_output, output_output, candidate_cell, current_cell, previous_cell,
            previous_hidden) = self.cache[t]

            hidden_gradient = next_hidden_state_gradient + previous_hidden_gradient
            cell_gradient = next_cell_state_gradient + previous_cell_gradient

            output_gradient = hidden_gradient * tanh(current_cell)
            output_raw_gradient = output_gradient * output_output * (1 - output_output)

            cell_gradient_t = cell_gradient + hidden_gradient * output_output * (1 - tanh(current_cell) ** 2)
            cell_candidate_gradient = cell_gradient_t * input_output
            cell_candidate_raw_gradient = cell_candidate_gradient * (1 - candidate_cell ** 2)

            input_gradient = cell_gradient_t * candidate_cell
            input_raw_gradient = input_gradient * input_output * (1 - input_output)

            forget_gradient = cell_gradient_t * previous_cell
            forget_raw_gradient = forget_gradient * forget_output * (1 - forget_output)

            gradient_forget_gate_weights += np.dot(forget_raw_gradient, concatenated_input.T)
            gradient_forget_gate_bias += forget_raw_gradient
            gradient_input_gate_weights += np.dot(input_raw_gradient, concatenated_input.T)
            gradient_input_gate_bias += input_raw_gradient
            gradient_output_gate_weights += np.dot(output_raw_gradient, concatenated_input.T)
            gradient_output_gate_bias += output_raw_gradient
            gradient_cell_state_weights += np.dot(cell_candidate_raw_gradient, concatenated_input.T)
            gradient_cell_state_bias += cell_candidate_raw_gradient

            concatenated_gradient = (
                    np.dot(self.forget_gate_weights.T, forget_raw_gradient) +
                    np.dot(self.input_gate_weights.T, input_raw_gradient) +
                    np.dot(self.output_gate_weights.T, output_raw_gradient) +
                    np.dot(self.cell_state_weights.T, cell_candidate_raw_gradient)
            )

            previous_hidden_gradient = concatenated_gradient[:self.hidden_size, :]
            previous_cell_gradient = cell_gradient_t * forget_output

        self.cache = []

        return (
        gradient_forget_gate_weights, gradient_forget_gate_bias, gradient_input_gate_weights, gradient_input_gate_bias,
        gradient_output_gate_weights, gradient_output_gate_bias, gradient_cell_state_weights, gradient_cell_state_bias)
