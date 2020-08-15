import configparser
import enum
import logging
from typing import Optional, List

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

logging.basicConfig(level=logging.DEBUG)


class DBConstructorQueries(enum.Enum):
    CREATE_DB = """
        CREATE DATABASE {};
        """

    DROP_DB = """
        DROP DATABASE {};
        """

    DB_EXISTS = """
        SELECT datname 
        FROM pg_database
        WHERE datname = '{}';     
        """

    KILL_ALL_CONNECTIONS = """
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{}'
        -- AND pid <> pg_backend_pid();   
        """

    CREATE_TABLE = """
        CREATE TABLE
        """


class DataBaseConstructor(object):
    default_db = "coronavirus_local"
    queries = DBConstructorQueries

    def __init__(
            self,
            config_path: str = "db/worldmeter.ini",
            db_name: str = default_db
    ) -> None:
        self.__paths: dict = self.read_config(
            config_path=config_path,
            section="paths"
        )
        self.current: Optional[str] = None
        self.connection = None
        self.cursor = None
        self.connect(db_name)

    def read_config(
            self,
            config_path: str = "db/worldmeter.ini",
            section: Optional[str] = None
    ) -> dict:
        """Returns a dict with configuration read from file with path given."""
        if section is None:
            section = self.default_db

        parser = configparser.ConfigParser()
        parser.read(config_path)

        config = dict()
        for key, value in parser.items(section):
            config[key] = value

        return config

    def connect(self, db_name: str = default_db) -> None:
        """Connects to database.

        Sets current instance attribute to the name of the database to which
        a successful connection has been established.

        Arguments:
            db_name: database name
            
        If no argument given, connects to default db.
        """

        conn = psycopg2.connect(**self.read_config(section=db_name))
        logging.info(f"Connected to database: {db_name}")

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.current = db_name
        self.connection = conn

    def read_query_from_file(self, filename: str) -> str:
        path = self.__paths["queries"] + filename
        with open(path, 'r') as query_file:
            query = query_file.read()
            logging.info(f"Query '{filename}' loaded successfuly.")
            return query

    def run_query(
            self,
            query: str,
            commit: bool = False,
            fetch_n: Optional[int] = None,
            next_query: bool = False
    ) -> List:
        """Runs a query.

        By default it is not committed. Can be committed by specifying 'commit'
        argument to True.

        Arguments:
            query: a query to run. Should be already filled with all needed
                parameters.
            commit: a boolean specifying whether the query should be committed.
            fetch_n: if None, an assumption is made, the query does not return
                any results. If 0, returns all results available. Else, returns
                the number of query results specified in the argument, starting
                at the beginning.
            next_query: a boolean specifying whether another query will be run
                after this query. If set to False the current query should not
                be committed. The cursor will remain open.
                It's useful to run queries in a group one after
                another when you want to have either all or none committed. In
                such case use 'self.run_queries_in_group_and_commit' function.

        Returns:
            List of fetched results in a form of tuples. If query returns no
            results, an empty list is returned.

        """
        self.cur = self.connection.cursor()
        fetched = []
        logging.info(fetched)
        try:
            logging.info(query)
            self.cur.execute(query)
            logging.info(query)

            if commit:
                self.connection.commit()
                logging.info(f"Query executed successfuly.")

            if fetch_n is not None:
                if fetch_n == 0:
                    fetched = self.cur.fetchall()
                else:
                    fetched = self.cur.fetchmany(fetch_n)
            if not next_query:
                self.cur.close()
                self.cur = None
        except psycopg2.DatabaseError as error:
            logging.error(error)
            logging.info(error)
        logging.info(fetched)
        return fetched

    def run_queries_in_group_and_commit(self, queries: List[str]):
        for query in queries:
            print(query)
            self.run_query(query, commit=False, next_query=True)
        self.connection.commit()
        self.cur.close()
        self.cur = None

    def insert_db_name(self, db_name: Optional[str], query: str) -> str:
        target_db = db_name if db_name else self.current
        logging.info(f"Target database set to: '{target_db}'...")
        return query.format(target_db)

    def drop_dp(self, db_name: Optional[str]) -> None:
        kill_connections_query = self.insert_db_name(
            db_name, self.queries.KILL_ALL_CONNECTIONS.value)
        drop_query = self.insert_db_name(db_name, self.queries.DROP_DB.value)
        logging.info(f"Running: Drop Database...")

        self.run_queries_in_group_and_commit([
            kill_connections_query,
            drop_query,
        ])

    def create_db(self, db_name: Optional[str]) -> None:
        logging.info(f"Running: Create Database...")
        query = self.insert_db_name(db_name, self.queries.CREATE_DB.value)
        self.run_query(query, commit=True)

    def reset_db(self, db_name: Optional[str]) -> None:
        self.drop_dp(db_name)
        self.create_db(db_name)
