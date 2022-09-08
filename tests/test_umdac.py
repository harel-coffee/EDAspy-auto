from unittest import TestCase
from EDAspy.optimization import UMDAc
from EDAspy.benchmarks import ContinuousBenchmarkingCEC14
import numpy as np


class TestUMDAc(TestCase):

    def test_constructor(self):
        n_variables = 10
        umda = UMDAc(size_gen=100, max_iter=100, dead_iter=10, n_variables=n_variables, alpha=0.5,
                     lower_bound=-10, elite_factor=0.2)

        assert umda.size_gen == 100
        assert umda.max_iter == 100
        assert umda.dead_iter == 10
        assert umda.n_variables == n_variables
        assert umda.alpha == 0.5

    def test_bounds(self):
        """Check if new individuals meet the bounds restrictions"""
        n_variables = 10
        umda = UMDAc(size_gen=10, max_iter=1, dead_iter=0, n_variables=n_variables, alpha=0.5,
                     lower_bound=-10, elite_factor=0.2, disp=False)

        benchmarking = ContinuousBenchmarkingCEC14(n_variables)

        umda.minimize(benchmarking.cec14_4, False)
        # data = umda.generation

        assert not np.any(umda.pm.pm[1, :] < umda.lower_bound)  # ensure the std has been modified

    def test_vector(self):
        n_variables = 10
        umda = UMDAc(size_gen=100, max_iter=100, dead_iter=10, n_variables=n_variables, alpha=0.5,
                     lower_bound=-10, elite_factor=0.2)

        assert umda.vector.shape == (2, n_variables)

        vector = np.zeros((2, n_variables))
        vector[0, :] = [0] * n_variables
        vector[1, :] = [9] * n_variables

        umda = UMDAc(size_gen=100, max_iter=100, dead_iter=10, n_variables=n_variables, alpha=0.5,
                     vector=vector, lower_bound=-10, elite_factor=0.2)

        assert umda.vector.shape == (2, n_variables)

    def test_new_generation(self):
        n_variables = 10
        umda = UMDAc(size_gen=100, max_iter=1, dead_iter=0, n_variables=n_variables, alpha=0.5)
        benchmarking = ContinuousBenchmarkingCEC14(n_variables)

        umda.minimize(benchmarking.cec14_4, False)

        assert umda.generation.shape[0] == umda.size_gen + (umda.size_gen * umda.elite_factor)

    def test_check_generation(self):
        n_vars = 10
        umda = UMDAc(size_gen=100, max_iter=100, dead_iter=10, n_variables=n_vars, alpha=0.5)

        gen = np.random.normal(
            [0]*umda.n_variables, [10]*umda.n_variables, [umda.size_gen, umda.n_variables]
        )
        umda.generation = gen
        benchmarking = ContinuousBenchmarkingCEC14(n_vars)
        umda._check_generation(benchmarking.cec14_4)
        assert len(umda.evaluations) == len(umda.generation)