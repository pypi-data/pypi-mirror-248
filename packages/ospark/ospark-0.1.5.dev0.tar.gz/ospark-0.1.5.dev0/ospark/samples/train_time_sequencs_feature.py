import pandas

from ospark.trainer.auto_encoder_trainer import AutoencoderTrainer
from ospark.data.generator.n_gram_datagenerator import NGramDataGenerator
from ospark.nn.block.transformer_block import transformer_encoder_block
from ospark.nn.layers.dense_layer import DenseLayer
from ospark.backbone.auto_encoder import PositionalEncodingAutoencoder
from ospark.nn.optimizer.learning_rate_schedule import TransformerWarmup
import tensorflow as tf



data_path = "/Users/donggicai1991/Documents/golden_model/GoldPassbook.csv"


data = pandas.read_csv(data_path, usecols=["日期", "本行賣出價格"])

train_data = []
for date_value_pair in zip(data["日期"], data["本行賣出價格"]):
    train_data.append({date_value_pair[0]: date_value_pair[1]})

data_generator = NGramDataGenerator(train_data=train_data,
                                    batch_size=4,
                                    n_gram=[5])

encoder = [DenseLayer(obj_name="linear_projection",
                      input_dimension=5,
                      hidden_dimension=[64, 128, 256])]
decoder = DenseLayer(obj_name="decoder",
                     input_dimension=256,
                     hidden_dimension=[128, 64, 5])

for i in range(4):
    obj_name = f"encoder_{i}"
    encoder.append(transformer_encoder_block(obj_name=obj_name,
                                             head_number=8,
                                             embedding_size=256,
                                             scale_rate=4,
                                             dropout_rate=0.1))

auto_encoder = PositionalEncodingAutoencoder(obj_name="auto_encoder",
                                             encoder=encoder,
                                             decoder=decoder,
                                             embedding_size=256)

loss_function = lambda prediction, target_data: tf.reduce_mean(tf.pow(prediction - target_data/100, 2))
# learning_rate = 0.000001
learning_rate = TransformerWarmup(model_dimension=256, warmup_step=4000.)
optimizer     = tf.keras.optimizers.legacy.Adam(learning_rate=learning_rate, beta_1=0.9, beta_2=0.98, epsilon=1e-9)

auto_encoder.create()

trainer = AutoencoderTrainer(model=auto_encoder,
                             data_generator=data_generator,
                             epoch_number=100,
                             save_times=5,
                             save_weights_path="./autoencoder_weights.json",
                             optimizer=optimizer,
                             loss_function=loss_function,
                             use_auto_graph=False)

trainer.start()

