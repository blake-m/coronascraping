import logging

import pandas as pd

from data_source.transformers import DataSource
from db.db import DataBase


class Inserter(object):
    def __init__(self, data_source: DataSource, db: DataBase):
        self.data_source = data_source
        self.db = db

    def insert(self, clean_start=False):
        # TODO(blake): multiprocessed/threaded?
        for country in self.data_source.data_as_dict:
            df_country = self.data_source.get_pandas_dataframe_for_one_country(
                country)
            country = country.replace('-', "_")
            df_country = df_country.drop([','], axis=1, errors='ignore')
            if clean_start:
                self.db.run_query(f"DROP TABLE {country}")

            self.db.create_table(
                table_name=country,
                columns=[(column, 'float', '')
                         for column in df_country.columns]
            )

            for index, row in df_country.iterrows():
                values = list(row.values)
                values = [
                    value if type(value) is str else '0' for value in values
                ]
                # TODO(blake): this is gonna break when the year changes
                index = pd.to_datetime("2020 " + index, format="%Y %b %d")

                values.insert(0, f"'{index}'")
                values = ', '.join(values)
                query = f"""
                    INSERT INTO {country}
                    VALUES ({values})
                    """
                logging.info(f"Query about to be run: \n{query}")
                self.db.run_query(query)
