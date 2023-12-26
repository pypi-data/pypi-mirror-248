from typing import Dict, Tuple, Optional, List
import copy
import tensorflow as tf
import numpy as np


class InformerDataGenerator:

    class Dataset:

        def __init__(self):
            self._encoder_input = None
            self._decoder_input = None
            self._target_data   = None
            self._time_stamps   = {}

        @property
        def encoder_input(self) -> tf.Tensor:
            return self._encoder_input

        @property
        def decoder_input(self) -> tf.Tensor:
            return self._decoder_input

        @property
        def target_data(self) -> tf.Tensor:
            return self._target_data

        @property
        def time_stamps(self) -> Dict[str, List[str]]:
            return self._time_stamps

        def setup_training_data(self,
                                encoder_input: tf.Tensor,
                                decoder_input: tf.Tensor,
                                target_data: tf.Tensor,
                                time_stamps: Dict[str, List[str]]):
            self._encoder_input = encoder_input
            self._decoder_input = decoder_input
            self._target_data = target_data
            self._time_stamps = time_stamps

    def __init__(self,
                 batch_size: int,
                 training_length: int,
                 predict_length: int,
                 training_data: List[Dict[str, float]],
                 initial_step: Optional[int]=None):
        self._training_length = training_length
        self._batch_size      = batch_size
        self._training_data   = training_data
        self._initial_step    = initial_step
        self._step            = 0
        self._dataset         = self.Dataset()
        self._data_length     = len(training_data)

        self._prediction_length       = predict_length
        self._prediction_record_start = training_length - predict_length

    def __iter__(self):
        return self

    def __next__(self):
        if self._step + self._training_length + self._prediction_length > self._data_length:
            raise StopIteration()
        dataset = self._get_data()
        self._step += 1
        return dataset

    def _get_data(self):
        training_start_point   = self._step
        training_end_point     = training_start_point + self._training_length
        prediction_start_point = training_start_point + self._prediction_record_start
        prediction_end_point   = prediction_start_point + 2 * self._prediction_length

        training_data  = self._training_data[training_start_point: training_end_point]
        target_dataset = self._training_data[prediction_start_point: prediction_end_point]

        encoder_input = tf.convert_to_tensor(list(map(lambda data: data["value"], training_data)), dtype=tf.float32)
        target_data   = list(map(lambda data: data["value"], target_dataset))
        decoder_input = np.array(copy.copy(target_data))

        decoder_input[self._prediction_length:] = 0
        encoder_input = tf.reshape(encoder_input, shape=[1, -1, 1])
        decoder_input = tf.reshape(tf.convert_to_tensor(decoder_input, dtype=tf.float32), shape=[1, -1, 1])
        target_data   = tf.reshape(tf.convert_to_tensor(target_data, dtype=tf.float32), shape=[1, -1, 1])

        time_stamps            = {}
        time_stamps["encoder"] = list(map(lambda data: data["time_stamp"], training_data))
        time_stamps["decoder"] = list(map(lambda data: data["time_stamp"], target_dataset))
        self._dataset.setup_training_data(encoder_input=encoder_input,
                                          decoder_input=decoder_input,
                                          target_data=target_data,
                                          time_stamps=time_stamps)
        return self._dataset



