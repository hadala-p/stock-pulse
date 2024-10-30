from unittest import TestCase

import numpy as np

from lstm.activations import sigmoid, tanh, relu


class TestActivations(TestCase):

    ############################ sigmoid ############################
    def test_sigmoid(self):
        assert np.isclose(sigmoid(0), 0.5)

    def test_sigmoid_negative(self):
        assert sigmoid(-100) < 0.01

    def test_sigmoid_positive(self):
        assert sigmoid(100) > 0.99

    def test_sigmoid_range(self):
        assert 0 < sigmoid(0.5) < 1

    def test_sigmoid_shape(self):
        assert sigmoid(np.array([-1, 0, 1])).shape == (3,)

    def test_sigmoid_type(self):
        assert isinstance(sigmoid(np.array([0])), np.ndarray)

    def test_sigmoid_zero(self):
        assert sigmoid(0) == 0.5

    ############################ tanh ############################
    def test_tanh(self):
        assert np.isclose(tanh(0), 0)

    def test_tanh_negative(self):
        assert tanh(-100) < -0.99

    def test_tanh_positive(self):
        assert tanh(100) > 0.99

    def test_tanh_range(self):
        assert -1 < tanh(0.5) < 1

    def test_tanh_shape(self):
        assert tanh(np.array([-1, 0, 1])).shape == (3,)

    def test_tanh_type(self):
        assert isinstance(tanh(np.array([0])), np.ndarray)

    def test_tanh_zero(self):
        assert tanh(0) == 0

    ############################ relu ############################

    def test_relu(self):
        assert relu(-1) == 0
        assert relu(1) == 1

    def test_relu_negative(self):
        assert relu(-100) == 0

    def test_relu_positive(self):
        assert relu(100) == 100

    def test_relu_range(self):
        assert 0 < relu(0.5) < 1

    def test_relu_shape(self):
        assert relu(np.array([-1, 0, 1])).shape == (3,)

    def test_relu_type(self):
        assert isinstance(relu(np.array([0])), np.ndarray)

    def test_relu_zero(self):
        assert relu(0) == 0
