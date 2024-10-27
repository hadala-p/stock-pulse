import unittest

import numpy as np

from lstm.lstm import LSTMModel
from lstm.optimizer import Adam


class TestLSTMModel(unittest.TestCase):
    def setUp(self):
        self.input_size = 5
        self.hidden_size = 3
        self.output_size = 2
        self.sequence_length = 4
        self.learning_rate = 0.01
        self.optimizer = Adam(learning_rate=self.learning_rate)
        self.model = LSTMModel(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            output_size=self.output_size,
            sequence_length=self.sequence_length,
            optimizer=self.optimizer
        )

    def test_forward_output_shape(self):
        x = np.random.randn(self.sequence_length, self.input_size)
        output, hidden_state = self.model.forward(x)

        self.assertEqual(output.shape, (self.output_size, 1))
        self.assertEqual(hidden_state.shape, (self.hidden_size, 1))

    def test_predict_output_shape(self):
        x = np.random.randn(self.sequence_length, self.input_size)
        output = self.model.predict(x)

        self.assertEqual(output.shape, (self.output_size, 1))

    def test_train_loss_decreases(self):
        x_train = [np.random.randn(self.sequence_length, self.input_size) for _ in range(10)]
        y_train = [np.random.randn(self.output_size, 1) for _ in range(10)]

        initial_loss = self._calculate_epoch_loss(x_train, y_train)

        self.model.train(x_train, y_train, epochs=5)

        final_loss = self._calculate_epoch_loss(x_train, y_train)

        self.assertLess(final_loss, initial_loss, "Final loss should be lower than initial loss after training")

    def _calculate_epoch_loss(self, x_data, y_data):
        epoch_loss = 0
        for x, y in zip(x_data, y_data):
            predicted_output, _ = self.model.forward(x)
            loss = np.mean((predicted_output - y) ** 2)
            epoch_loss += loss
        return epoch_loss / len(x_data)

    def test_gradient_shapes(self):
        x = np.random.randn(self.sequence_length, self.input_size)
        y = np.random.randn(self.output_size, 1)

        predicted_output, hidden_state = self.model.forward(x)

        output_gradient = 2 * (predicted_output - y) / y.size
        gradient_output_weights = np.dot(output_gradient, hidden_state.T)
        gradient_output_bias = output_gradient

        self.assertEqual(gradient_output_weights.shape, self.model.output_weights.shape)
        self.assertEqual(gradient_output_bias.shape, self.model.output_bias.shape)

    def test_optimizer_updates(self):
        x = np.random.randn(self.sequence_length, self.input_size)
        y = np.random.randn(self.output_size, 1)

        predicted_output, hidden_state = self.model.forward(x)

        output_gradient = 2 * (predicted_output - y) / y.size
        gradient_output_weights = np.dot(output_gradient, hidden_state.T)
        gradient_output_bias = output_gradient

        initial_output_weights = self.model.output_weights.copy()
        initial_output_bias = self.model.output_bias.copy()

        self.model.optimizer.update(
            [self.model.output_weights, self.model.output_bias],
            [gradient_output_weights, gradient_output_bias]
        )

        self.assertFalse(np.array_equal(self.model.output_weights, initial_output_weights))
        self.assertFalse(np.array_equal(self.model.output_bias, initial_output_bias))
