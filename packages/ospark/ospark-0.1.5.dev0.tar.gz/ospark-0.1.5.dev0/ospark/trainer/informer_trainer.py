from . import *
from ospark.models.informer import Informer


class InformerTrainer(Trainer):

    def __init__(self,
                 model: Informer,
                 data_generator: DataGenerator,
                 epoch_number: int,
                 optimizer: Optimizer,
                 loss_function: Union[LossFunction, Dict[str, LossFunction]],
                 save_weights_path: str,
                 save_info_path: str,
                 presentation_of_loss_value: Optional[int]=None,
                 save_delegate: Optional[SaveDelegate]=None,
                 save_times: Optional[int]=None,
                 use_auto_graph: Optional[bool]=True,
                 use_multi_gpu: Optional[bool]=None,
                 devices: Optional[List[str]]=None,
                 logger: Optional[Union[Logger, str]]=None):
        """
        Args:
            model:
            data_generator:
            epoch_number:
            optimizer:
            loss_function:
            save_weights_path:
            save_info_path:
            presentation_of_loss_value:
            save_delegate:
            save_times:
            use_auto_graph:
            use_multi_gpu:
            devices:
            logger:
        """

        super().__init__(model=model,
                         data_generator=data_generator,
                         epoch_number=epoch_number,
                         optimizer=optimizer,
                         loss_function=loss_function,
                         save_weights_path=save_weights_path,
                         save_info_path=save_info_path,
                         presentation_of_loss_value=presentation_of_loss_value,
                         save_delegate=save_delegate,
                         save_times=save_times,
                         use_auto_graph=use_auto_graph,
                         use_multi_gpu=use_multi_gpu,
                         devices=devices,
                         logger=logger)

    @property
    def model(self) -> Informer:
        return self._model

    def training_process(self) -> NoReturn:
        for epoch in range(self.epoch_number):
            total_loss_value = 0
            training_count = 0
            start_time = time.time()
            for step, dataset in enumerate(self.data_generator):
                prediction, target_data, loss_value = self.training_method(dataset)

                total_loss_value += loss_value
                training_count   += 1
                if self._presentation_of_loss_value is not None and step % self._presentation_of_loss_value == 0:
                    self._logger.info(f"step: {step}, loss value : {total_loss_value / training_count}")
                    self._logger.info("estimated time pre epoch: ",
                                      self.data_generator.max_step / (step + 1) * (time.time() - start_time))

            self._logger.info(f'Epoch {epoch + 1}, '
                              f'Loss {total_loss_value / training_count:.4f}')
            self._logger.info(f'Time taken for 1 epoch: {time.time() - start_time:.2f} secs\n')
            if self.will_save(epoch_number=epoch) and self.save_weights_path is not None:
                self.save_delegate.save(save_obj=self.weights_operator.weights, path=self.save_weights_path)
                self.save_delegate.save(save_obj=self.model.get_model_info(), path=self.save_info_path)

        if self.save_weights_path is not None:
            self.save_delegate.save(save_obj=self.weights_operator.weights, path=self.save_weights_path)
            self.save_delegate.save(save_obj=self.model.get_model_info(), path=self.save_info_path)

    def forward(self, dataset: DataGenerator.Dataset) -> Tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
        encoder_input, decoder_input, time_stamps = dataset.encoder_input, dataset.decoder_input, dataset.time_stamps
        target_data = dataset.target_data
        prediction = self.model.pipeline(encoder_input=encoder_input,
                                         encoder_time_stamps=time_stamps["encoder"],
                                         decoder_input=decoder_input,
                                         decoder_time_stamps=time_stamps["decoder"])
        loss_value = self.loss_function(prediction=prediction, target_data=target_data)
        return prediction, target_data, loss_value
