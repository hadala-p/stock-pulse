import numpy as np

from src.lstm.layers import LSTMLayer


class LSTMModel:
    def __init__(self, input_size, hidden_size, output_size, sequence_length, optimizer):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.sequence_length = sequence_length
        self.lstm_layer = LSTMLayer(input_size, hidden_size)
        self.output_weights = np.random.randn(output_size, hidden_size) * 0.01
        self.output_bias = np.zeros((output_size, 1))
        self.optimizer = optimizer

    def forward(self, x):
        hidden_state = np.zeros((self.hidden_size, 1))
        cell_state = np.zeros((self.hidden_size, 1))

        for t in range(self.sequence_length):
            input_timestep = x[t].reshape(self.input_size, 1)
            hidden_state, cell_state = self.lstm_layer.forward(input_timestep, hidden_state, cell_state)

        return np.dot(self.output_weights, hidden_state) + self.output_bias

    def train(self, x_train, y_train, epochs=100):
        for epoch in range(epochs):
            epoch_loss = 0
            for i in range(len(x_train)):
                input_sequence = x_train[i]
                true_output = y_train[i]

                # Forward pass
                predicted_output = self.forward(input_sequence)
                epoch_loss += np.mean((predicted_output - true_output) ** 2)

                # Backpropagation
                output_gradient = 2 * (predicted_output - true_output)

                output_weight_gradient = np.dot(output_gradient, input_sequence[-1].T)

                self.optimizer.update([self.output_weights, self.output_bias],
                                      [output_weight_gradient, output_gradient])
