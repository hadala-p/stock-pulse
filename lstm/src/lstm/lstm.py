from typing import Tuple

import numpy as np
from numpy.typing import NDArray

from lstm.layers import LSTMLayer
from lstm.optimizer import Adam


class LSTMModel:
    def __init__(self, input_size: int, hidden_size: int, output_size: int, sequence_length: int,
                 optimizer: Adam) -> None:

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.sequence_length = sequence_length
        self.lstm_layer = LSTMLayer(input_size, hidden_size)
        self.output_weights = np.random.randn(output_size, hidden_size) * 0.01
        self.output_bias = np.zeros((output_size, 1))
        self.optimizer = optimizer
        self.hidden_state: NDArray[np.float64] = np.zeros((self.hidden_size, 1))
        self.cell_state: NDArray[np.float64] = np.zeros((self.hidden_size, 1))

    def forward(self, x: NDArray[np.float64], training = False) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        for t in range(self.sequence_length):
            input_timestep: NDArray[np.float64] = x[t].reshape(self.input_size, 1)
            self.hidden_state, self.cell_state = self.lstm_layer.forward(input_timestep, self.hidden_state, self.cell_state, training)

        output: NDArray[np.float64] = np.dot(self.output_weights, self.hidden_state) + self.output_bias
        return output, self.hidden_state

    def reset_states(self):
        self.hidden_state = np.zeros((self.hidden_size, 1))
        self.cell_state = np.zeros((self.hidden_size, 1))

    def train(self, x_train, y_train, epochs=100):
        for epoch in range(epochs):
            epoch_loss = 0
            for i in range(len(x_train)):
                input_sequence = x_train[i]
                true_output = y_train[i]
                predicted_output, hidden_state = self.forward(input_sequence, training=True)

                loss = np.mean((predicted_output[0][0] - true_output) ** 2)
                if i % 10 == 0:
                     print(f"[Training {i}/{len(x_train)}] Precicted: {predicted_output}, Actual: {true_output}")                 
                epoch_loss += loss

                output_gradient = 2 * (predicted_output - true_output) / true_output.size

                gradient_output_weights = np.dot(output_gradient, hidden_state.T)
                gradient_output_bias = output_gradient

                next_hidden_gradient = np.dot(self.output_weights.T, output_gradient)
                next_cell_gradient = np.zeros_like(next_hidden_gradient)

                lstm_gradients = self.lstm_layer.backward(next_hidden_gradient, next_cell_gradient)

                (gradient_forget_gate_weights,
                 gradient_forget_gate_bias,
                 gradient_input_gate_weights,
                 gradient_input_gate_bias,
                 gradient_output_gate_weights,
                 gradient_output_gate_bias,
                 gradient_cell_state_weights,
                 gradient_cell_state_bias) = lstm_gradients

                params = [
                    self.output_weights, self.output_bias,
                    self.lstm_layer.forget_gate_weights, self.lstm_layer.forget_gate_bias,
                    self.lstm_layer.input_gate_weights, self.lstm_layer.input_gate_bias,
                    self.lstm_layer.output_gate_weights, self.lstm_layer.output_gate_bias,
                    self.lstm_layer.cell_state_weights, self.lstm_layer.cell_state_bias
                ]
                grads = [
                    gradient_output_weights, gradient_output_bias,
                    gradient_forget_gate_weights, gradient_forget_gate_bias,
                    gradient_input_gate_weights, gradient_input_gate_bias,
                    gradient_output_gate_weights, gradient_output_gate_bias,
                    gradient_cell_state_weights, gradient_cell_state_bias
                ]
                self.optimizer.update(params, grads)
            self.reset_states()    
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss / len(x_train)}")