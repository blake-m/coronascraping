import abc
import enum
import logging
from typing import List, Optional, Tuple


class Methods(abc.ABC):
    def run_query(
            self,
            query: str,
            commit: bool = False,
            fetch_n: Optional[int] = None,
            next_query: bool = False
    ) -> List:
        pass


class CRUDMethodsBase(enum.Enum):
    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS {} (
            {}
            {}
        );
        """


class CRUDMethods(Methods):
    queries = CRUDMethodsBase

    def create_table(
            self,
            table_name: str,
            columns: List[Tuple[str, str, str]],
            table_constraints: List[str] = None,
            db_name: Optional[str] = None
    ):
        query_columns = [' '.join(column) for column in columns]
        query_columns = [column.replace('-', '_') for column in query_columns]
        query_columns = ', '.join(query_columns)

        query_constraints = []
        if table_constraints is not None:
            query_constraints.append(',')
            for constraint in table_constraints:
                query_constraints.append(constraint)
            query_constraints = ''.join(query_constraints)
        query_base = self.queries.CREATE_TABLE.value

        query = [query_base] \
                + [table_name] \
                + ['(date VARCHAR(32) UNIQUE, '] \
                + [query_columns] \
                + query_constraints \
                + [')']
        query = ' '.join(query)

        self.run_query(query)
        logging.info(f"Table '{table_name}' created.")
