try:
    from db_python_manager.data_source.transformers import DataSource
    from db_python_manager.db.db import DataBase
except ModuleNotFoundError:
    from data_source.transformers import DataSource
    from db.db import DataBase


class Inserter(object):
    def __init__(self, data_source: DataSource, db: DataBase):
        self.data_source = data_source
        self.db = db

    def insert(self, clean_start=False):
        # TODO(blake): multiprocessed?

        for country in self.data_source.data_as_dict:
            df_country = self.data_source.get_pandas_dataframe_for_one_country(
                country)
            country = country.replace('-', "_")
            if clean_start:
                self.db.run_query(f"DROP TABLE {country}")
                self.db.create_table(
                    table_name=country,
                    columns=[(column, 'float', '')
                             for column in df_country.columns]
                )

            for index, row in df_country.iterrows():
                values = list(row.values)
                values = [value if type(value) is str else '0' for value in values ]
                values.insert(0, f"'{index}'")
                print(values)
                values = ', '.join(values)
                query = f"""
                    INSERT INTO {country}
                    VALUES ({values})
                    """
                self.db.run_query(query)






