from __future__ import annotations

import random

from ospark.data.generator import DataGenerator
from typing import Optional, Union, List, Dict
import tensorflow as tf
import math

class SequenceDataGenerator(DataGenerator):

    class Dataset:

        def __init__(self):
            pass

    def __init__(self, training_data: Union[tf.Tensor, list], batch_size: int, init_step: Optional[int]=None):
        super().__init__(training_data=training_data,
                         target_data=None,
                         batch_size=batch_size,
                         initial_step=init_step)

    def _get_data(self) -> Dataset:
        raise NotImplementedError()


class NGramDataGenerator(SequenceDataGenerator):

    class Dataset:

        def __init__(self):
            self._training_data = None
            self._timestamps    = None

        @property
        def training_data(self) -> tf.Tensor:
            return self._training_data

        @property
        def timestamps(self) -> List[str]:
            return self._timestamps

        def setting_dataset(self, training_data: tf.Tensor, timestamps: List[str]):
            self._training_data = training_data
            self._timestamps    = timestamps

    def __init__(self,
                 train_data: Union[tf.Tensor, List[Dict[str, str]]],
                 batch_size: int,
                 n_gram: List[int],
                 init_step: Optional[int]=None):
        super().__init__(training_data=train_data, batch_size=batch_size, init_step=init_step)
        self._n_gram      = n_gram
        self._data_length = len(train_data)

        self._max_step = math.ceil(len(train_data) - max(n_gram)) / batch_size if type(train_data) == list else math.ceil(train_data.shape[0] / batch_size)
        self._step     = 0
        self._dataset  = self.Dataset()

    @property
    def n_gram(self) -> List[int]:
        return self._n_gram

    @property
    def dataset(self) -> Dataset:
        return self._dataset

    def _get_data(self) -> Dataset:
        date_data     = []
        sequence_data = []

        start_point = self.step * self.batch_size
        if len(self.n_gram) > 1:
            samples = random.sample(self.n_gram, self.batch_size)
        else:
            samples = self.n_gram * self.batch_size
        max_length  = max(samples)
        for i, sample in enumerate(samples):
            dates  = []
            values = []
            end_point = min(start_point + i + sample, self._data_length)
            for _data in self.training_data[start_point + i: end_point][::-1]:
                date, value = list(_data.items())[0]
                date        = str(date)
                dates.append(f"{date[:4]}-{date[4:6]}-{date[6:]}")
                values.append(value)

            while len(dates) != max_length:
                    dates.append("None")
                    values.append(0)

            date_data.append(dates)
            sequence_data.append(values)

        self.dataset.setting_dataset(training_data=sequence_data, timestamps=date_data)
        return self.dataset