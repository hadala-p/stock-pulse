from unittest import TestCase

import numpy as np

from lstm.activations import sigmoid, tanh
from lstm.layers import LSTMLayer


class TestLSTMLayer(TestCase):
    def setUp(self):
        self.input_size = 4
        self.hidden_size = 3
        self.dropout_rate = 0.2
        self.layer = LSTMLayer(self.input_size, self.hidden_size, self.dropout_rate)

    def test_forward_output_shapes(self):
        x = np.random.randn(self.input_size, 1)
        h_prev = np.random.randn(self.hidden_size, 1)
        c_prev = np.random.randn(self.hidden_size, 1)

        h, c = self.layer.forward(x, h_prev, c_prev)

        self.assertEqual(h.shape, (self.hidden_size, 1))
        self.assertEqual(c.shape, (self.hidden_size, 1))

    def test_forward_computation(self):
        # Ustawienie dropout_rate na 0.0, na czas testu
        self.layer.dropout_rate = 0.0

        x = np.random.randn(self.input_size, 1)
        h_prev = np.random.randn(self.hidden_size, 1)
        c_prev = np.random.randn(self.hidden_size, 1)

        h, c = self.layer.forward(x, h_prev, c_prev)
        concatenated_input = np.vstack((h_prev, x))

        f_gate = sigmoid(np.dot(self.layer.forget_gate_weights, concatenated_input) + self.layer.forget_gate_bias)
        i_gate = sigmoid(np.dot(self.layer.input_gate_weights, concatenated_input) + self.layer.input_gate_bias)
        o_gate = sigmoid(np.dot(self.layer.output_gate_weights, concatenated_input) + self.layer.output_gate_bias)
        candidate_c = tanh(np.dot(self.layer.cell_state_weights, concatenated_input) + self.layer.cell_state_bias)

        expected_c = f_gate * c_prev + i_gate * candidate_c
        expected_h = o_gate * tanh(expected_c)

        np.testing.assert_almost_equal(h, expected_h, decimal=5)
        np.testing.assert_almost_equal(c, expected_c, decimal=5)

    def test_forward_with_dropout(self):
        x = np.random.randn(self.input_size, 1)
        h_prev = np.random.randn(self.hidden_size, 1)
        c_prev = np.random.randn(self.hidden_size, 1)

        self.layer.dropout_rate = 0.5
        h, _ = self.layer.forward(x, h_prev, c_prev)

        dropout_applied = (h == 0).sum()
        self.assertTrue(dropout_applied > 0)

    def test_backward_output_shapes(self):
        x = np.random.randn(self.input_size, 1)
        h_prev = np.random.randn(self.hidden_size, 1)
        c_prev = np.random.randn(self.hidden_size, 1)

        self.layer.forward(x, h_prev, c_prev)
        d_next_h = np.random.randn(self.hidden_size, 1)
        d_next_c = np.random.randn(self.hidden_size, 1)

        grads = self.layer.backward(d_next_h, d_next_c)
        grad_shapes = [
            grads[0].shape, grads[1].shape, grads[2].shape, grads[3].shape,
            grads[4].shape, grads[5].shape, grads[6].shape, grads[7].shape
        ]

        expected_shapes = [
            (self.hidden_size, self.input_size + self.hidden_size), (self.hidden_size, 1),
            (self.hidden_size, self.input_size + self.hidden_size), (self.hidden_size, 1),
            (self.hidden_size, self.input_size + self.hidden_size), (self.hidden_size, 1),
            (self.hidden_size, self.input_size + self.hidden_size), (self.hidden_size, 1)
        ]

        for grad_shape, expected_shape in zip(grad_shapes, expected_shapes):
            self.assertEqual(grad_shape, expected_shape)

    def test_backward_computation(self):
        x = np.random.randn(self.input_size, 1)
        h_prev = np.random.randn(self.hidden_size, 1)
        c_prev = np.random.randn(self.hidden_size, 1)

        self.layer.forward(x, h_prev, c_prev)
        d_next_h = np.random.randn(self.hidden_size, 1)
        d_next_c = np.random.randn(self.hidden_size, 1)

        grads = self.layer.backward(d_next_h, d_next_c)

        for grad in grads:
            self.assertIsInstance(grad, np.ndarray)
            self.assertTrue(np.all(np.isfinite(grad)))
