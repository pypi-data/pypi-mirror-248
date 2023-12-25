# -*- coding: utf-8 -*-

from typing import Dict, List, Tuple, Iterator, Any, Self, Type

from core_mixins.interfaces.factory import IFactory


class DatabaseClient(IFactory):
    """ Base class for all database clients """

    _impls: Dict[str, Type[Self]] = {}

    # Mapper for python types to database engine type...
    type_mapper = {}

    def __init__(self, **kwargs):
        super(DatabaseClient, self).__init__()

        self._parameters = kwargs
        self.connection = None
        self.cursor = None

        # Function used by the library to perform
        # the connection to the engine...
        self.connect_fcn = None

    def __enter__(self) -> Self:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self) -> None:
        """ Connects to the database engine """

        try:
            self.connection = self.connect_fcn(**self._parameters)

        except Exception as error:
            raise DatabaseClientException(error)

    def test_connection(self, query: str):
        """ Tests the connection """

    def execute(self, query: str):
        """ Executes the query """

    def fetch_all(self) -> Iterator[Dict[str, Any]]:
        """
        Because the fetchall operation returns a list of tuples (no headers), you can use
        this function to retrieve the data in the form of dictionary...
        """

    @classmethod
    def get_create_ddl(cls, table_fqn: str, columns: List[Tuple[str, str]], temporal: bool = False) -> str:
        """
        Returns the SQL statement to create a table...

        :param table_fqn    -- Table's full qualifier name.
        :param columns      -- List of tuples defining the name and data type for the attribute...
        :param temporal     -- Defines if is a temporal table.

        :return: The query statement.
        """

    def insert_records(
            self, table_fqn: str, columns: List, records: List[Dict],
            records_per_request: int = 500) -> int:

        """
        Insert data into the database...

        :param table_fqn: Table's fully qualified name (FQN).
        :param columns: List of columns.
        :param records: Records to insert.
        :param records_per_request: Number of records to insert per call.

        :return: Return the number of inserted records.
        """

    @staticmethod
    def get_insert_dml(table_fqn: str, columns: List, records: List[Dict]) -> str:
        """
        Create the query for the INSERT statement.

        :param table_fqn: Table's fully qualified name (FQN).
        :param columns: List of columns.
        :param records: List of records.
        :return: Query.
        """

    def delete(self, table_fqn: str, records: List[Dict], column_id: str, timestamp_col: str):
        """ Delete records """

    @staticmethod
    def get_delete_dml(
            table_fqn: str, records: List[Dict], column_id: str = None,
            timestamp_col: str = None) -> str:

        """ Creates the DELETE statement """

    def merge(self, table_fqn: str, records: List[Dict], id_columns: List[str], epoch_column: str):
        """ Insert/Update process """

    def close(self):
        if self.connection:
            self.connection.close()


class DatabaseClientException(Exception):
    """ Custom exception for Database Client """
