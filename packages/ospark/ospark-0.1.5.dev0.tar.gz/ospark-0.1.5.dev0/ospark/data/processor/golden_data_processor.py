from ospark.data.processor.auto_click import AutoClick
import pandas
import pathlib


class GoldenDataProcessor(metaclass=AutoClick):

    def __init__(self,
                 data_path: str,
                 save_folder: str,
                 save_file_name: str,
                 n_gram: int):
        self._data_path      = data_path
        self._save_folder    = save_folder
        self._save_file_name = save_file_name
        self._save_path      = pathlib.Path(save_folder) / save_file_name
        self._n_gram         = n_gram

    def main_process(self):
        golden_data = pandas.read_csv(self._data_path, usecols=["日期", "本行賣出價格"])
        golden_data.get()

    def n_gram_process(self, data: pandas.DataFrame):

    def target_process(self):