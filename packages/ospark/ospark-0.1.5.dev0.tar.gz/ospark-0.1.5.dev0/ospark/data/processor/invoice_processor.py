from ospark.data.processor.auto_click import AutoClick
from typing import Optional, List
from functools import reduce
import ndjson
import pathlib
import json


class InvoiceDataProcessor(metaclass=AutoClick):
    """
    Invoice data processor.
    """

    def __init__(self,
                 images_path: str,
                 recoder_json_path: str,
                 save_folder: str,
                 save_file_name: str,
                 mapping_table_path: Optional[str]=None):
        """
        Args:
            images_path: str
            recoder_json_path: str
            save_folder: str
            save_file_name: str
            mapping_table_path: Optional[str]
        """

        self._image_path            = images_path
        self._recoder_json_path     = recoder_json_path
        self._save_folder           = pathlib.Path(save_folder)
        self._save_file_name        = save_file_name
        self._corpus_save_path      = self._save_folder / "corpus.json"
        self._target_data_save_path = self._save_folder / save_file_name

        if mapping_table_path is not None:
            with open(mapping_table_path, 'r') as fp:
                mapping_table = json.load(fp)
        else:
            mapping_table = None

        self._mapping_table = mapping_table or {"invoice_type": "發票種類",
                                                "date": "發票日期",
                                                "id_number": "發票號碼",
                                                "sales_amount": "銷售金額",
                                                "sales_tax": "銷售稅",
                                                "total": "總計",
                                                "buyer_tax": "買方統編",
                                                "seller_tax": "賣方統編",
                                                "tax_status": "課稅別"}

        self._file_name_mapping_table = {str(file_name).split("_")[-1]: file_name for file_name in pathlib.Path(images_path).iterdir()
                                         if str(file_name).split("/")[-1][0] != "."}

    def main_process(self):
        dataset = []
        for file_name in pathlib.Path(self._recoder_json_path).iterdir():
            if str(file_name).split("_")[-1] == "recorder.json":
                try:
                    with open(file_name, 'r') as fp:
                        json_data = json.load(fp)
                except:
                    continue

                for name, info in json_data.items():
                    processed_data = {}
                    image_name = info["image_name"]
                    if image_name not in self._file_name_mapping_table:
                        continue
                    name   = self._file_name_mapping_table[image_name]
                    target = reduce(lambda init_value, tax_info: init_value + f"{tax_info[1]}: {self.data_priority(info.get(tax_info[0]))}。", self._mapping_table.items(), "")
                    processed_data["image_path"]  = str(name)
                    processed_data["target_data"] = target
                    dataset.append(processed_data)

        corpus = self.create_corpus(dataset=dataset)

        with open(self._corpus_save_path, 'w') as fp:
            json.dump(corpus, fp)

        with open(self._target_data_save_path, 'w') as fp:
            ndjson.dump(dataset, fp)

    def data_priority(self, data: dict) -> str:
        """
        Logical judgment of data priority and then obtaining the corresponding data.

        Args:
            data: dict

        Returns:
            value: str
        """

        if data is None:
            return ""

        if data.get("checked_value") is not None:
            value = data.get("checked_value")
        else:
            value = data["adjusted_value"] if data["adjusted_value"] != "" else data["value"]

        return value

    def create_corpus(self, dataset: List[dict]) -> dict:
        """
        Create corpus.

        Args:
            dataset: List[dict]

        Returns:
            corpus: dict
        """

        corpus = {"PAD": 0, "CLS": 1, "BOS": 2, "EOS": 3}
        for data in dataset:
            for char in data["target_data"]:
                corpus.setdefault(char, len(corpus))
        return corpus


if __name__ == "__main__":
    InvoiceDataProcessor()