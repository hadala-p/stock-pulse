import numpy as np


class LSTMLayer:
    def __init__(self, input_size, hidden_size):

        # Initialize weights and biases for gates
        self.forget_gate_weights = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.forget_gate_bias = np.zeros((hidden_size, 1))

        self.input_gate_weights = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.input_gate_bias = np.zeros((hidden_size, 1))

        self.output_gate_weights = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.output_gate_bias = np.zeros((hidden_size, 1))

        self.cell_state_weights = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.cell_state_bias = np.zeros((hidden_size, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def tanh(self, x):
        return np.tanh(x)

    def forward(self, x, previous_hidden_state, previous_cell_state):
        concatenated_input = np.vstack((previous_hidden_state, x))

        forget_gate_output = self.sigmoid(np.dot(self.forget_gate_weights, concatenated_input) + self.forget_gate_bias)

        input_gate_output = self.sigmoid(np.dot(self.input_gate_weights, concatenated_input) + self.input_gate_bias)

        output_gate_output = self.sigmoid(np.dot(self.output_gate_weights, concatenated_input) + self.output_gate_bias)

        candidate_cell_state = self.tanh(np.dot(self.cell_state_weights, concatenated_input) + self.cell_state_bias)
        updated_cell_state = forget_gate_output * previous_cell_state + input_gate_output * candidate_cell_state

        updated_hidden_state = output_gate_output * self.tanh(updated_cell_state)

        return updated_hidden_state, updated_cell_state
