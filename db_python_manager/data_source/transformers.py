import abc
import configparser
import enum
import json
from abc import ABC

import pandas as pd

pd.set_option('display.max_columns', 10)

CONFIG_PATH = 'config.ini'


class DataSource(abc.ABC):
    def __init__(self, config_path):
        self.config: configparser.ConfigParser = self.load_config(config_path)
        self.data = self.connect_to_data()
        self.data_as_dict = self.convert_data_source_to_dict()


    @abc.abstractmethod
    def load_config(self, config_path: str):
        pass

    @abc.abstractmethod
    def connect_to_data(self):
        pass

    @abc.abstractmethod
    def convert_data_source_to_dict(self):
        pass

    @abc.abstractmethod
    def get_pandas_dataframe_for_one_country(self, country):
        pass


class JSONDataSource(DataSource):
    def load_config(self, config_path: str):
        cfg = configparser.ConfigParser()
        cfg.read(config_path)
        return cfg

    def connect_to_data(self):
        try:
            path = self.config['DEFAULT']["PathData"]
            with open(path, 'rb') as file:
                json_loaded = json.load(file)
        except FileNotFoundError:
            path = self.config["DEFAULT"]["PathDataLocal"]
            with open(path, 'rb') as file:
                json_loaded = json.load(file)
        return json_loaded

    def convert_data_source_to_dict(self):
        countries_dict = {}
        for dictionary in self.data:
            for key, value in dictionary.items():
                countries_dict[key] = value
        return countries_dict

    def get_pandas_dataframe_for_one_country(self, country):
        country_dict = self.data_as_dict[country]
        df = pd.DataFrame(country_dict)
        return df


def main():
    data_source = JSONDataSource(CONFIG_PATH)
    for c in data_source.data_as_dict:
        print(data_source.data_as_dict[c])


if __name__ == "__main__":
    main()
