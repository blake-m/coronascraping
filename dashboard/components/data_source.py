import abc
import configparser
import json
import logging
from typing import List, Tuple

import pandas as pd
import psycopg2

pd.set_option('display.max_columns', 10)

CONFIG_PATH = '../config.ini'


class DataSource(abc.ABC):
    def __init__(self, config_path: str, section: str):
        self.config: configparser.ConfigParser = self.load_config(config_path)
        self.config = self.config[section]
        self.connection = self.connect_to_data()

    @staticmethod
    def load_config(config_path: str) -> configparser.ConfigParser:
        cfg = configparser.ConfigParser()
        cfg.read(config_path)
        return cfg

    @abc.abstractmethod
    def connect_to_data(self):
        pass

    @abc.abstractmethod
    def get_pandas_dataframe_for_one_country(self, country: str):
        pass

    @abc.abstractmethod
    def get_countries(self):
        pass


class JSONDataSource(DataSource):
    def __init__(self, config_path):
        super().__init__(config_path, "JSON")
        self.data = self.connection

    def connect_to_data(self):
        path = self.config["PathData"]
        with open(path, 'rb') as file:
            json_loaded = json.load(file)
        return json_loaded

    def convert_json_list_to_dict(self):
        countries_dict = {}
        for dictionary in self.connection:
            for key, value in dictionary.items():
                countries_dict[key] = value
        return countries_dict

    def get_pandas_dataframe_for_one_country(self, country: str):
        countries_dict = self.convert_json_list_to_dict()
        country_dict = countries_dict[country]
        df = pd.DataFrame(country_dict)
        return df

    def get_pandas_dataframe_for_all_countries(self):
        countries_dict = self.convert_json_list_to_dict()
        dfs = []
        for country, graphs in countries_dict.items():
            for graph, data in graphs.items():
                df = pd.DataFrame.from_dict(data, orient='index').transpose()
                dfs.append(df)
        df = pd.concat(dfs)
        return df

    def get_countries(self):
        countries = []
        for country in self.connection:
            for key in country:
                if key != "world-population":
                    # TODO(blake) - separate dashes and capitalize
                    countries.append(key)
        return countries


class PostgresDataSource(DataSource):
    def __init__(self, config_path):
        super().__init__(config_path, "POSTGRES")

    def read_db_config(self) -> dict:
        """Returns a dict with configuration read from file with path given."""

        config = dict()
        for key, value in self.config.items():
            config[key] = value

        return config

    def run_query(self, query: str) -> List[Tuple]:
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def connect_to_data(self) -> psycopg2.extensions.connection:
        """Connects to database.

        Sets current instance attribute to the name of the database to which
        a successful connection has been established.

        Arguments:
            db_name: database name

        If no argument given, connects to default db.
        """
        connection = psycopg2.connect(**self.read_db_config())
        logging.info("Connected to database.")
        return connection

    def get_pandas_dataframe_for_one_country(self, country: str) -> pd.DataFrame:
        query_values = f"SELECT * FROM {country}"
        data = self.run_query(query_values)

        query_column_names = f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
                AND table_name='{country}';
        """
        column_names = self.run_query(query_column_names)
        column_names = [column_tuple[0] for column_tuple in column_names]

        df = pd.DataFrame(data=data, columns=column_names)
        df = df.set_index("date")
        return df

    def get_countries(self):
        query_get_countries_names = """
            SELECT table_name 
            FROM information_schema.tables
            WHERE table_schema='public'
        """
        return sorted([
            country_tuple[0] for country_tuple
            in self.run_query(query_get_countries_names)
        ])


def main():
    data_source = PostgresDataSource(CONFIG_PATH)
    # data_source = JSONDataSource(CONFIG_PATH)
    country = data_source.get_pandas_dataframe_for_one_country("poland")
    countries = data_source.get_countries()


if __name__ == "__main__":
    main()
