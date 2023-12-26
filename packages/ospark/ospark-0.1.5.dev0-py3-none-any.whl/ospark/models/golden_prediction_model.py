from ospark.nn.model import Model
from ospark.backbone.auto_encoder import PositionalEncodingAutoencoder
from typing import Optional
from ospark.nn.block.informer_block import informer_decoder_block
import tensorflow as tf


class GoldenPredictionModel(Model):

    def __init__(self,
                 obj_name: str,
                 auto_encoder: PositionalEncodingAutoencoder,
                 block_number: int,
                 head_number: int,
                 embedding_size: int,
                 scale_rate:int,
                 dropout_rate: float,
                 is_training: Optional[bool]=None,
                 training_phase: Optional[bool]=None):
        super().__init__(obj_name=obj_name, is_training=is_training, training_phase=training_phase)
        self._auto_encoder   = auto_encoder
        self._block_number   = block_number
        self._head_number    = head_number
        self._embedding_size = embedding_size
        self._scale_rate     = scale_rate
        self._dropout_rate   = dropout_rate
        self._classify_layer = None

        self.block = informer_decoder_block(obj_nam="decoder_block",
                                            head_number=head_number,
                                            scale_rate=scale_rate,
                                            embedding_size=embedding_size,
                                            is_training=is_training,
                                            dropout_rate=dropout_rate,
                                            sample_factor=5.0)

        # if classification_number is not None:
        #     self._classify_layer = DenseLayer(obj_name="classify_layer",
        #                                       input_dimension=embedding_size,
        #                                       hidden_dimension=[embedding_size / 2,
        #                                                         embedding_size / 4,
        #                                                         classification_number])

    def pipeline(self, input_data) -> tf.Tensor:
        feature_map = self._auto_encoder.pipeline(input_data=input_data)

        decoder_output = self.block.pipeline(input_data=feature_map)
        prediction = self._auto_encoder.decoder.pipeline(input_data=decoder_output)

        return prediction