import abc
import configparser
import enum
import json
from abc import ABC

import pandas as pd

pd.set_option('display.max_columns', 10)

CONFIG_PATH = 'config.ini'


class GraphTypes(enum.Enum):
    CASES = 'coronavirus-cases-linear'


class CountriesAvailable(enum.Enum):
    POLAND = 'poland'
    UK = 'uk'
    US = 'us'


class DataSource(abc.ABC):
    def __init__(self, config_path):
        self.config: configparser.ConfigParser = self.load_config(config_path)
        self.data = self.connect_to_data()

    @abc.abstractmethod
    def load_config(self, config_path: str):
        pass

    @abc.abstractmethod
    def connect_to_data(self):
        pass

    @abc.abstractmethod
    def get_pandas_dataframe_for_one_country(self, country, graph_types):
        pass

    @abc.abstractmethod
    def get_pandas_dataframe_for_all_countries(self):
        pass


class JSONDataSource(DataSource):
    def load_config(self, config_path: str):
        cfg = configparser.ConfigParser()
        cfg.read(config_path)
        return cfg

    def connect_to_data(self):
        path = self.config['DEFAULT']["PathData"]
        with open(path, 'rb') as file:
            json_loaded = json.load(file)
        return json_loaded

    def convert_json_list_to_dict(self):
        countries_dict = {}
        for dictionary in self.data:
            for key, value in dictionary.items():
                countries_dict[key] = value
        return countries_dict

    def get_pandas_dataframe_for_one_country(self, country: GraphTypes, graph_types):
        countries_dict = self.convert_json_list_to_dict()
        country_dict = countries_dict[country]
        df = pd.DataFrame(country_dict)
        return df

    def get_pandas_dataframe_for_all_countries(self):
        countries_dict = self.convert_json_list_to_dict()
        dfs = []
        for country, graphs in countries_dict.items():
            # print(key, countries_dict[key])
            for graph, data in graphs.items():
                # print(country, graph, data)
                df = pd.DataFrame.from_dict(data, orient='index').transpose()
                # df.set_index(graph)
                dfs.append(df)
        df = pd.concat(dfs)



        # df = pd.DataFrame.from_dict(countries_dict, orient='index')
        print(df)
        return df


class PostgresDataSource(DataSource, ABC):
    pass


class Country(object):
    def __init__(self, data_source: DataSource, country: CountriesAvailable):
        self.data_source = data_source
        self.graph_types = GraphTypes
        self.country = country
        self.data = self.__get_data()

    def check_if_data_available(self):
        pass

    def __get_data(self):
        return self.data_source.get_pandas_dataframe_for_one_country(
            self.country, self.graph_types)


def main():
    data_source = JSONDataSource(CONFIG_PATH)
    # data_source.get_pandas_dataframe_for_all_countries()
    poland = Country(data_source, CountriesAvailable.POLAND.value)
    print(poland.data)


if __name__ == "__main__":
    main()
