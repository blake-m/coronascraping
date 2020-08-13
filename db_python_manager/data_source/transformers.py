import abc
import configparser
import json
import os
from typing import Dict

import pandas as pd

pd.set_option('display.max_columns', 10)

CONFIG_PATH = 'data_source/config.ini'


class DataSource(abc.ABC):
    def __init__(self, data_source_file: str):
        self.config: configparser.ConfigParser = self.load_config(CONFIG_PATH)
        self.data = self.connect_to_data(data_source_file)
        self.data_as_dict = self.convert_data_source_to_dict()

    @staticmethod
    def load_config(config_path: str) -> configparser.ConfigParser:
        cfg = configparser.ConfigParser()
        cfg.read(config_path)
        return cfg

    @abc.abstractmethod
    def connect_to_data(self, data_source_file: str) -> Dict:
        pass

    def convert_data_source_to_dict(self) -> Dict:
        countries_dict = {}
        for dictionary in self.data:
            for key, value in dictionary.items():
                countries_dict[key] = value
        return countries_dict

    def get_pandas_dataframe_for_one_country(
            self, country: str) -> pd.DataFrame:
        country_dict = self.data_as_dict[country]
        df = pd.DataFrame(country_dict)
        return df


class JSONDataSource(DataSource):
    def connect_to_data(self, data_source_file: str) -> Dict:
        path = os.path.join(
            self.config['DEFAULT']['DataFolder'], data_source_file)
        with open(path, 'rb') as file:
            print(path)
            return json.load(file)
