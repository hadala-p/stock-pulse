from unittest import TestCase

import numpy as np

from lstm.optimizer import Adam


class TestAdam(TestCase):
    def setUp(self):
        self.learning_rate = 0.001
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.epsilon = 1e-8
        self.optimizer = Adam(
            learning_rate=self.learning_rate,
            beta1=self.beta1,
            beta2=self.beta2,
            epsilon=self.epsilon,
        )
        self.params = [np.array([0.5, -0.3]), np.array([1.5, -1.2])]
        self.grads = [np.array([0.1, -0.1]), np.array([0.2, -0.2])]

    def test_update_shapes(self):
        initial_params = [param.copy() for param in self.params]
        self.optimizer.update(self.params, self.grads)

        for param, initial_param in zip(self.params, initial_params):
            self.assertEqual(param.shape, initial_param.shape)

    def test_update_values(self):
        initial_params = [param.copy() for param in self.params]
        self.optimizer.update(self.params, self.grads)

        for param, initial_param in zip(self.params, initial_params):
            self.assertFalse(
                np.array_equal(param, initial_param),
                "Parameters should update after one step",
            )

    def test_first_moment_estimate(self):
        self.optimizer.update(self.params, self.grads)
        for m, grad in zip(self.optimizer.first_moment_estimate, self.grads):
            expected_m = self.beta1 * 0 + (1 - self.beta1) * grad
            np.testing.assert_array_almost_equal(m, expected_m, decimal=5)

    def test_second_moment_estimate(self):
        self.optimizer.update(self.params, self.grads)
        for v, grad in zip(self.optimizer.second_moment_estimate, self.grads):
            expected_v = self.beta2 * 0 + (1 - self.beta2) * (grad**2)
            np.testing.assert_array_almost_equal(v, expected_v, decimal=5)

    def test_iteration_increments(self):
        initial_iteration = self.optimizer.iteration
        self.optimizer.update(self.params, self.grads)
        self.assertEqual(self.optimizer.iteration, initial_iteration + 1)

    def test_learning_rate_adjustment(self):
        initial_iteration = self.optimizer.iteration
        self.optimizer.update(self.params, self.grads)

        lr_adjusted = self.learning_rate * (
            np.sqrt(1 - self.beta2 ** (initial_iteration + 1))
            / (1 - self.beta1 ** (initial_iteration + 1))
        )

        self.assertAlmostEqual(
            lr_adjusted,
            self.learning_rate
            * (
                np.sqrt(1 - self.beta2**self.optimizer.iteration)
                / (1 - self.beta1**self.optimizer.iteration)
            ),
            places=5,
            msg="Adjusted learning rate should match the computed value",
        )

    def test_update_stabilizes_with_repeated_calls(self):
        for _ in range(1000):  # Symuluje dużą liczbę iteracji
            self.optimizer.update(self.params, self.grads)

        for param in self.params:
            self.assertTrue(
                np.all(np.abs(param) < 10),
                "Parameters should not diverge with Adam updates",
            )
