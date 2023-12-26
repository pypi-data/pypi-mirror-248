from typing import Optional, Tuple

import numpy as np


class EarlyStopMechanism:

    def __init__(self, check_range: Optional[int]=None):
        self._check_range = check_range or 3
        self._temp_result = []
        self._variations  = []
        self._is_storage  = False
        self._is_continue = True

    def pipeline(self, validation_result: dict) -> Tuple[bool, bool]:
        raise NotImplementedError()


class LossEarlyStop(EarlyStopMechanism):

    def __init__(self, variation_threshold: Optional[float]=None, check_range: Optional[int]=None):
        super().__init__(check_range=check_range)
        self._variation_threshold = variation_threshold or 0.01

    def pipeline(self, validation_result: dict) -> Tuple[bool, bool]:

        self._temp_result.append(validation_result["loss_value"])

        if len(self._temp_result) > 1:
            self._variations.append(self._temp_result[-2] - self._temp_result[-1])

        if np.mean(self._variations[-self._check_range]) > 0:
            self._is_continue = False
            self._is_storage  = False
        elif np.mean(np.abs(self._variations[-self._check_range])) <= self._variation_threshold:
            self._is_continue = False
            self._is_storage  = True
        elif self._variations[-1] > -self._variation_threshold:
            self._is_continue = True
            self._is_storage  = True
        else:
            self._is_storage  = False
            self._is_continue = True
        return self._is_storage, self._is_continue


class AccuracyEarlyStop(EarlyStopMechanism):

    def __init__(self, variation_threshold: Optional[float]=None, check_range: Optional[int]=None):
        super().__init__(check_range=check_range)
        self._variation_threshold = variation_threshold or 0.05

    def pipeline(self, validation_result: dict) -> Tuple[bool, bool]:

        self._temp_result.append(validation_result["loss_value"])

        if len(self._temp_result) > 1:
            self._variations.append(self._temp_result[-2] - self._temp_result[-1])

        if np.mean(self._variations[-self._check_range]) < 0:
            self._is_continue = False
            self._is_storage  = False
        elif np.mean(np.abs(self._variations[-self._check_range])) <= self._variation_threshold:
            self._is_continue = False
            self._is_storage  = True
        elif self._variations[-1] < self._variation_threshold:
            self._is_continue = True
            self._is_storage  = True
        else:
            self._is_storage  = False
            self._is_continue = True
        return self._is_storage, self._is_continue