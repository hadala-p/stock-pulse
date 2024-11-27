from typing import Tuple

import numpy as np
from numpy.typing import NDArray

from lstm.layers import LSTMLayer
from lstm.optimizer import Adam
from lstm.model_saver import save_model
import random


class LSTMModel:
    def __init__(self, input_size: int, hidden_sizes: list[int], output_size: int, sequence_length: int, optimizer: Adam) -> None:
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.sequence_length = sequence_length
        self.lstm_layers = [
            LSTMLayer(input_size if i == 0 else hidden_sizes[i - 1], hidden_size, dropout_rate=0.01)
            for i, hidden_size in enumerate(hidden_sizes)
        ]
        self.output_weights = np.random.randn(output_size, hidden_sizes[-1]) * 0.01
        self.output_bias = np.zeros((output_size, 1))
        self.optimizer = optimizer
        self.best_loss = float('inf')

    def forward(self, x: NDArray[np.float64], training=False) -> Tuple[NDArray[np.float64], list[NDArray[np.float64]]]:
        hidden_states = [np.zeros((hidden_size, 1)) for hidden_size in self.hidden_sizes]
        cell_states = [np.zeros((hidden_size, 1)) for hidden_size in self.hidden_sizes]

        # Process the input sequence through the stacked LSTM layers
        for t in range(self.sequence_length):
            input_timestep = x[t].reshape(self.input_size, 1)
            for i, lstm_layer in enumerate(self.lstm_layers):
                input_timestep, cell_states[i] = lstm_layer.forward(
                    input_timestep, hidden_states[i], cell_states[i], training
                )
                hidden_states[i] = input_timestep

        # Compute output using the final hidden state of the last LSTM layer
        output = np.dot(self.output_weights, hidden_states[-1]) + self.output_bias
        return output, hidden_states

    def train(self, x_train, y_train, epochs=100, new_stock_data = False):
        for epoch in range(epochs):
            epoch_loss = 0
            random_data_indexes = list(range(len(x_train)))
            random.shuffle(random_data_indexes)
            index = 0
            for i in random_data_indexes:
                index +=1
                input_sequence = x_train[i]
                true_output = y_train[i].reshape(-1, 1)
                predicted_output, hidden_states = self.forward(input_sequence, training=True)

                # Compute Mean Squared Error Loss
                loss = np.mean((predicted_output - true_output) ** 2)
                if index % 50 == 0:
                    print(f"[Training] {index}/{len(random_data_indexes)} Loss: {loss}")
                epoch_loss += loss

                # Compute gradients for backpropagation
                output_gradient = 2 * (predicted_output - true_output) / true_output.size
                gradient_output_weights = np.dot(output_gradient, hidden_states[-1].T)
                gradient_output_bias = output_gradient

                # Gradients for hidden and cell states of the last LSTM layer
                next_hidden_gradient = np.dot(self.output_weights.T, output_gradient)
                next_cell_gradient = np.zeros_like(next_hidden_gradient)

                # Backpropagate through LSTM layers in reverse order
                lstm_gradients = []
                for i in reversed(range(len(self.lstm_layers))):
                    lstm_layer = self.lstm_layers[i]
                    lstm_grad = lstm_layer.backward(next_hidden_gradient, next_cell_gradient)
                    lstm_gradients.append(lstm_grad)
                    # Unpack the gradients returned by the backward method
                    (
                        gradient_forget_gate_weights, gradient_forget_gate_bias,
                        gradient_input_gate_weights, gradient_input_gate_bias,
                        gradient_output_gate_weights, gradient_output_gate_bias,
                        gradient_cell_state_weights, gradient_cell_state_bias,
                        hidden_gradient, cell_gradient
                    ) = lstm_grad

                    # Update `next_hidden_gradient` for the previous layer
                    next_hidden_gradient = hidden_gradient

                    # Update `next_cell_gradient` for the previous layer
                    next_cell_gradient = cell_gradient

                # Update parameters using optimizer
                params = [self.output_weights, self.output_bias]
                grads = [gradient_output_weights, gradient_output_bias]
                for layer, layer_grads in zip(self.lstm_layers, reversed(lstm_gradients)):
                    params.extend([
                        layer.forget_gate_weights, layer.forget_gate_bias,
                        layer.input_gate_weights, layer.input_gate_bias,
                        layer.output_gate_weights, layer.output_gate_bias,
                        layer.cell_state_weights, layer.cell_state_bias
                    ])
                    grads.extend(layer_grads)
                self.optimizer.update(params, grads)

            mean_loss = epoch_loss / len(x_train)
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {mean_loss}")
            if mean_loss < self.best_loss or new_stock_data:
                self.best_loss = mean_loss
                new_stock_data = False
                print(f"Found new best model with loss: {self.best_loss}. Saving to a file")
                model_data = LSTMModelData(self)
                save_model(model_data, 'model.sp')

        print(f"Training complete. Best loss: {self.best_loss}")

class LSTMModelData:
    def __init__(self, model: LSTMModel) -> None:
        self.output_weights = model.output_weights
        self.output_bias = model.output_bias
        self.lstm_layers_data = [
            {
                'forget_gate_weights': layer.forget_gate_weights,
                'forget_gate_bias': layer.forget_gate_bias,
                'input_gate_weights': layer.input_gate_weights,
                'input_gate_bias': layer.input_gate_bias,
                'output_gate_weights': layer.output_gate_weights,
                'output_gate_bias': layer.output_gate_bias,
                'cell_state_weights': layer.cell_state_weights,
                'cell_state_bias': layer.cell_state_bias
            }
            for layer in model.lstm_layers
        ]
        self.best_loss = model.best_loss

    def apply_to_model(self, model: LSTMModel) -> None:
        model.output_weights = self.output_weights
        model.output_bias = self.output_bias
        for layer, layer_data in zip(model.lstm_layers, self.lstm_layers_data):
            layer.forget_gate_weights = layer_data['forget_gate_weights']
            layer.forget_gate_bias = layer_data['forget_gate_bias']
            layer.input_gate_weights = layer_data['input_gate_weights']
            layer.input_gate_bias = layer_data['input_gate_bias']
            layer.output_gate_weights = layer_data['output_gate_weights']
            layer.output_gate_bias = layer_data['output_gate_bias']
            layer.cell_state_weights = layer_data['cell_state_weights']
            layer.cell_state_bias = layer_data['cell_state_bias']
        model.best_loss = self.best_loss
