from unittest import TestCase

import numpy as np

from lstm.loss import MeanSquaredError, CrossEntropyLoss


class TestMeanSquaredError(TestCase):
    def test_forward_zero_loss(self):
        predicted = np.array([1.0, 2.0, 3.0])
        actual = np.array([1.0, 2.0, 3.0])
        loss = MeanSquaredError.forward(predicted, actual)
        self.assertAlmostEqual(loss, 0.0, places=5)

    def test_forward_nonzero_loss(self):
        predicted = np.array([1.0, 2.0, 3.0])
        actual = np.array([1.0, 2.0, 4.0])
        loss = MeanSquaredError.forward(predicted, actual)
        self.assertAlmostEqual(loss, 1 / 3, places=5)

    def test_backward_gradient(self):
        predicted = np.array([1.0, 2.0, 3.0])
        actual = np.array([1.0, 2.0, 4.0])
        gradient = MeanSquaredError.backward(predicted, actual)
        expected_gradient = 2 * (predicted - actual) / actual.size
        np.testing.assert_array_almost_equal(gradient, expected_gradient, decimal=5)


class TestCrossEntropyLoss(TestCase):
    def test_forward_zero_loss(self):
        predicted = np.array([[0.7, 0.3], [0.2, 0.8]])
        actual = np.array([[1, 0], [0, 1]])
        loss = CrossEntropyLoss.forward(predicted, actual)
        self.assertAlmostEqual(loss, -np.mean(np.log(predicted[actual == 1])), places=5)

    def test_forward_nonzero_loss(self):
        predicted = np.array([[0.6, 0.4], [0.3, 0.7]])
        actual = np.array([[1, 0], [0, 1]])
        loss = CrossEntropyLoss.forward(predicted, actual)
        expected_loss = -np.sum(actual * np.log(predicted)) / predicted.shape[0]
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_backward_gradient(self):
        predicted = np.array([[0.6, 0.4], [0.3, 0.7]])
        actual = np.array([[1, 0], [0, 1]])
        gradient = CrossEntropyLoss.backward(predicted, actual)
        epsilon = 1e-12
        clipped_predicted = np.clip(predicted, epsilon, 1.0 - epsilon)
        expected_gradient = -(actual / clipped_predicted) / actual.shape[0]
        np.testing.assert_array_almost_equal(gradient, expected_gradient, decimal=5)
