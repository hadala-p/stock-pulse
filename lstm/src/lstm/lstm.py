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

    def forward(self, x: NDArray[np.float64]) -> NDArray[np.float64]:

        hidden_state: NDArray[np.float64] = np.zeros((self.hidden_size, 1))
        cell_state: NDArray[np.float64] = np.zeros((self.hidden_size, 1))

        for t in range(self.sequence_length):
            input_timestep: NDArray[np.float64] = x[t].reshape(self.input_size, 1)
            hidden_state, cell_state = self.lstm_layer.forward(input_timestep, hidden_state, cell_state)

        output: NDArray[np.float64] = np.dot(self.output_weights, hidden_state) + self.output_bias
        return output

    def train(self, x_train: NDArray[np.float64], y_train: NDArray[np.float64], epochs: int = 100) -> None:

        for epoch in range(epochs):
            epoch_loss: float = 0
            for i in range(len(x_train)):
                input_sequence: NDArray[np.float64] = x_train[i]
                true_output: NDArray[np.float64] = y_train[i]

                # Forward pass
                predicted_output: NDArray[np.float64] = self.forward(input_sequence)

                loss: float = np.mean((predicted_output - true_output) ** 2)
                epoch_loss += loss

                # Backpropagation
                output_gradient: NDArray[np.float64] = 2 * (predicted_output - true_output)

                output_weight_gradient: NDArray[np.float64] = np.dot(output_gradient, input_sequence[-1].T)

                self.optimizer.update([self.output_weights, self.output_bias],
                                      [output_weight_gradient, output_gradient])
