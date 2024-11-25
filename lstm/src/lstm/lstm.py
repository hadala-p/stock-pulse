from typing import Tuple

import numpy as np
from numpy.typing import NDArray

from lstm.layers import LSTMLayer
from lstm.optimizer import Adam
import random


class LSTMModel:
    def __init__(self, input_size: int, hidden_size: int, output_size: int, sequence_length: int,
                 optimizer: Adam) -> None:
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.sequence_length = sequence_length
        self.lstm_layer = LSTMLayer(input_size, hidden_size, dropout_rate=0.01)
        self.output_weights = np.random.randn(output_size, hidden_size) * 0.01
        self.output_bias = np.zeros((output_size, 1))
        self.optimizer = optimizer
        self.best_loss = float('inf')

    def load_model(self, model_data) -> None:
        self.output_weights = model_data.output_weights
        self.output_bias = model_data.output_bias
        self.lstm_layer.forget_gate_weights = model_data.forget_gate_weights
        self.lstm_layer.forget_gate_bias = model_data.forget_gate_bias
        self.lstm_layer.input_gate_weights = model_data.input_gate_weights
        self.lstm_layer.input_gate_bias = model_data.input_gate_bias
        self.lstm_layer.output_gate_weights = model_data.output_gate_weights
        self.lstm_layer.output_gate_bias = model_data.output_gate_bias
        self.lstm_layer.cell_state_weights = model_data.cell_state_weights
        self.lstm_layer.cell_state_bias = model_data.cell_state_bias
        self.best_loss = model_data.best_loss

    def forward(self, x: NDArray[np.float64], training=False) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        hidden_state: NDArray[np.float64] = np.zeros((self.hidden_size, 1))
        cell_state: NDArray[np.float64] = np.zeros((self.hidden_size, 1))

        # Process the input sequence through the LSTM
        for t in range(self.sequence_length):
            input_timestep: NDArray[np.float64] = x[t].reshape(self.input_size, 1)
            hidden_state, cell_state = self.lstm_layer.forward(input_timestep, hidden_state, cell_state, training)

        # Compute output using output weights and bias
        output: NDArray[np.float64] = np.dot(self.output_weights, hidden_state) + self.output_bias
        return output, hidden_state

    def train(self, x_train, y_train, epochs=100):
        better_training_found = False
        for epoch in range(epochs):
            epoch_loss = 0
            random_data_indexes = list(range(len(x_train)))
            random.shuffle(random_data_indexes)
            index = 0
            for i in random_data_indexes:
                index += 1
                input_sequence = x_train[i]
                true_output = y_train[i].reshape(-1, 1)
                predicted_output, hidden_state = self.forward(input_sequence, training=True)

                # Compute Mean Squared Error Loss
                loss = np.mean((predicted_output - true_output) ** 2)
                if index % 50 == 0:
                    print(f"[Training] {index}/{len(random_data_indexes)} Loss: {loss}")
                epoch_loss += loss

                # Compute gradients for backpropagation
                output_gradient = 2 * (predicted_output - true_output) / true_output.size

                # Gradients for output weights and bias
                gradient_output_weights = np.dot(output_gradient, hidden_state.T)
                gradient_output_bias = output_gradient

                # Gradients for hidden and cell states
                next_hidden_gradient = np.dot(self.output_weights.T, output_gradient)
                next_cell_gradient = np.zeros_like(next_hidden_gradient)

                # Backpropagate through the LSTM layer
                lstm_gradients = self.lstm_layer.backward(next_hidden_gradient, next_cell_gradient)

                # Unpack LSTM layer gradients
                (gradient_forget_gate_weights, gradient_forget_gate_bias,
                 gradient_input_gate_weights, gradient_input_gate_bias,
                 gradient_output_gate_weights, gradient_output_gate_bias,
                 gradient_cell_state_weights, gradient_cell_state_bias) = lstm_gradients

                # Combine parameters and gradients for optimizer update
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
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss / len(x_train)}")
            if (epoch_loss / len(x_train)) < self.best_loss:
                better_training_found = True
                self.best_loss = epoch_loss / len(x_train)
                best_output_weights = self.output_weights
                best_output_bias = self.output_bias
                best_forget_gate_weights = self.lstm_layer.forget_gate_weights
                best_forget_gate_bias = self.lstm_layer.forget_gate_bias
                best_input_gate_weights = self.lstm_layer.input_gate_weights
                best_input_gate_bias = self.lstm_layer.input_gate_bias
                best_output_gate_weights = self.lstm_layer.output_gate_weights
                best_output_gate_bias = self.lstm_layer.output_gate_bias
                best_cell_state_weights = self.lstm_layer.cell_state_weights
                best_cell_state_bias = self.lstm_layer.cell_state_bias
        if better_training_found:
            print(f"Training finished. Found and applying better learnables with loss: {self.best_loss}")
            self.output_weights = best_output_weights
            self.output_bias = best_output_bias
            self.lstm_layer.forget_gate_weights = best_forget_gate_weights
            self.lstm_layer.forget_gate_bias = best_forget_gate_bias
            self.lstm_layer.input_gate_weights = best_input_gate_weights
            self.lstm_layer.input_gate_bias = best_input_gate_bias
            self.lstm_layer.output_gate_weights = best_output_gate_weights
            self.lstm_layer.output_gate_bias = best_output_gate_bias
            self.lstm_layer.cell_state_weights = best_cell_state_weights
            self.lstm_layer.cell_state_bias = best_cell_state_bias
        else:
            print(f"Training finished. Best loss: {self.best_loss}. Better learnables not found.")
               

class LSTMModelData:
    def __init__(self, model: LSTMModel) -> None:
        self.output_weights = model.output_weights
        self.output_bias = model.output_bias
        self.forget_gate_weights = model.lstm_layer.forget_gate_weights
        self.forget_gate_bias = model.lstm_layer.forget_gate_bias
        self.input_gate_weights = model.lstm_layer.input_gate_weights
        self.input_gate_bias = model.lstm_layer.input_gate_bias
        self.output_gate_weights = model.lstm_layer.output_gate_weights
        self.output_gate_bias = model.lstm_layer.output_gate_bias
        self.cell_state_weights = model.lstm_layer.cell_state_weights
        self.cell_state_bias = model.lstm_layer.cell_state_bias
        self.best_loss = model.best_loss
