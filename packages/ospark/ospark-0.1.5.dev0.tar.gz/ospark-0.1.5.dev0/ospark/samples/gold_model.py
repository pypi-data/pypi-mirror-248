import pathlib
import csv
from ospark.data.generator.informer_data_generator import InformerDataGenerator
from ospark.trainer.informer_trainer import InformerTrainer
from ospark.models.builder import FormerBuilder
from ospark.nn.optimizer.learning_rate_schedule import TransformerWarmup
import tensorflow as tf


def mse_loss(prediction, target):
    loss_value = tf.math.sqrt(tf.reduce_mean(tf.math.square(target - prediction)))
    return loss_value

data_path     = "/Users/donggicai1991/Documents/golden_model/GoldPassbook.csv"
training_data = []
with open(data_path, 'r', encoding = 'utf-8-sig') as fp:
    reader = csv.DictReader(fp)

    for row in reader:
        data = {}
        time_stamp = row["日期"]
        time_stamp = f"{time_stamp[:4]}-{time_stamp[4:6]}-{time_stamp[6:]}"
        value = row["本行賣出價格"]
        data["value"] = float(value)
        data["time_stamp"] = time_stamp
        training_data.append(data)

model = FormerBuilder.informer(class_number=1,
                               block_number=4,
                               embedding_size=256,
                               head_number=8,
                               scale_rate=4,
                               sample_factor=0.1,
                               dropout_rate=0.1,
                               trained_weights=None,
                               is_training=True,
                               use_decoder=True,
                               use_classify_layer=True)

data_generator = InformerDataGenerator(batch_size=1,
                                       training_data=training_data[::-1],
                                       training_length=5,
                                       predict_length=3,
                                       )

loss_function = mse_loss

learning_rate = TransformerWarmup(model_dimension=256,
                                  warmup_step=4000)
optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=learning_rate,
                                            beta_1=0.9,
                                            beta_2=0.98,
                                            epsilon=1e-9)
trainer = InformerTrainer(model=model,
                          data_generator=data_generator,
                          epoch_number=1,
                          logger=None,
                          loss_function=loss_function,
                          optimizer=optimizer,
                          save_weights_path="./weights.json",
                          save_info_path="./info.json",
                          use_auto_graph=False)

trainer.start()