#!/usr/bin/env python
# coding: utf-8

import numpy as np
from .probabilistic_model import ProbabilisticModel


class UniGauss(ProbabilisticModel):

    def __init__(self, variables: list, std_bound: float):
        super().__init__(variables)

        self.pm = np.zeros((2, self.len_variables))
        self._std_bound = std_bound

        self.id = 1

    def sample(self, size: int):
        dataset = np.random.normal(
            self.pm[0, :], self.pm[1, :], [size, self.len_variables]
        )
        return dataset

    def learn(self, dataset: np.array):
        for i in range(len(self.variables)):
            self.pm[0, i] = np.mean(dataset[:, i])
            self.pm[1, i] = np.std(dataset[:, i])

            if self.pm[1, i] < self._std_bound:
                self.pm[1, i] = self._std_bound

    @property
    def pm(self):
        return self._pm

    @pm.setter
    def pm(self, value: np.array):
        assert value.shape == (2, len(self.variables)), "The argument must have a shape of 2 x number of variables."
        self._pm = value
