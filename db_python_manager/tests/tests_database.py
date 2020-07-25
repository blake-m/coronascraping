import configparser
import os
import unittest
from unittest import mock

import psycopg2

try:
    from db_python_manager.db import constructor, db, methods

    MODULES_PATH = "db_python_manager.db"
except ModuleNotFoundError:
    from db import constructor, db, methods

    MODULES_PATH = "db"


class TestDataBaseConstructorReadConfig(unittest.TestCase):
    def setUp(self) -> None:
        mock_path = MODULES_PATH + ".constructor.DataBaseConstructor.__init__"
        self.config_path = "stubs/worldmeter_db.cfg"
        with mock.patch(mock_path) as init:
            init.return_value = None
            self.db = constructor.DataBaseConstructor()

    def test_read_config_returns_dict(self):
        config = self.db.read_config(config_path=self.config_path,
                                     section="DEFAULT")
        self.assertIs(dict, type(config))

    def test_read_config_returns_dict_with_keys_from_config(self):
        config = self.db.read_config(config_path=self.config_path,
                                     section="DEFAULT")
        print(type(config["key"]))
        self.assertEqual("value", config["key"])

    def test_read_config_raises_error_when_config_section_not_found(self):
        with self.assertRaises(configparser.NoSectionError):
            config = self.db.read_config(config_path=self.config_path)


class TestDataBaseConstructorConnectToDB(unittest.TestCase):
    @mock.patch(MODULES_PATH + ".constructor.DataBaseConstructor.read_config")
    def setUp(self, read_config) -> None:
        read_config.return_value = dict(
            database='postgres',
            user='postgres',
            host='localhost',
            password='postgres',
            port='5432',
        )
        self.db = constructor.DataBaseConstructor("cfg_path")

    def test_connect_to_db_returns_connection(self):
        self.assertIs(self.db.connection, psycopg2.extensions.connection)


if __name__ == '__main__':
    unittest.main()
