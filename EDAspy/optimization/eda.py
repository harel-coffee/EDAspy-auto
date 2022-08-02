#!/usr/bin/env python
# coding: utf-8

import numpy as np
from abc import ABC, abstractmethod


class EDA(ABC):

    def __init__(self,
                 size_gen: int,
                 max_iter: int,
                 dead_iter: int,
                 n_variables: int,
                 alpha: float = 0.5,
                 elite_factor: float = 0.4,
                 disp: bool = True):

        self.disp = disp
        self.size_gen = size_gen
        self.max_iter = max_iter
        self.alpha = alpha
        self.n_variables = n_variables
        self.truncation_length = int(size_gen * alpha)
        self.elite_factor = elite_factor

        assert dead_iter <= self.max_iter, 'dead_iter must be lower than max_iter'
        self.dead_iter = dead_iter

        self.best_mae_global = 999999999999
        self.best_ind_global = -1
        self.evaluations = np.array(0)

        self.generation = np.zeros((self.size_gen, self.n_variables))

    @abstractmethod
    def _new_generation(self):
        raise Exception("Not implemented method")

    def _truncation(self):
        """
        Selection of the best individuals of the actual generation.
        """
        best_indices = self.evaluations.argsort()[: self.truncation_length]
        self.generation = self.generation[best_indices, :]
        self.evaluations = np.take(self.evaluations, best_indices)

    # check each individual of the generation
    def _check_generation(self, objective_function):
        """
        Check the cost of each individual in the cost function implemented by the user, and updates the
        generation DataFrame.
        """
        self.evaluations = np.apply_along_axis(objective_function, 1, self.generation)

    @abstractmethod
    def _update_pm(self):
        raise Exception("Not implemented method")

    # run the class to find the optimum
    def minimize(self, cost_function: callable, output_runtime: bool = True):
        r"""
        Args:
            cost_function: Cost function to be optimized and accepts an array as argument.
            output_runtime: True if information during runtime is desired.
        """

        history = []
        not_better = 0

        for _ in range(self.max_iter):
            self._check_generation(cost_function)
            self._truncation()
            self._update_pm()

            best_mae_local = min(self.evaluations)

            history.append(best_mae_local)
            best_ind_local = np.where(self.evaluations == best_mae_local)[0][0]
            best_ind_local = self.generation[best_ind_local]

            # update the best values ever
            if best_mae_local < self.best_mae_global:
                self.best_mae_global = best_mae_local
                self.best_ind_global = best_ind_local
                not_better = 0

            else:
                not_better += 1
                if not_better == self.dead_iter:
                    break

            self._new_generation()

            if output_runtime:
                print('IT: ', _, '\tBest cost: ', self.best_mae_global)

        if self.disp:
            print("\tNFVALS = " + str(len(history) * self.size_gen) + " F = " + str(self.best_mae_global))
            print("\tX = " + str(self.best_ind_global))

        return self.best_ind_global, self.best_mae_global, len(history) * self.size_gen
