# -*- coding: utf-8 -*-

import json
from typing import Any, Dict, Iterator, List, Tuple

from core_mixins.utils import get_batches

from .base import DatabaseClient
from .base import DatabaseClientException


class SqlDatabaseClient(DatabaseClient):
    """ Base class for all SQL based database clients """

    def __init__(self, **kwargs):
        super(SqlDatabaseClient, self).__init__(**kwargs)

        # Function used by the Database Engine
        # to convert to timestamp...
        self.epoch_to_timestamp_fcn = None

    def test_connection(self, query: str):
        try:
            return self.execute(query)

        except Exception as error:
            raise DatabaseClientException(error)

    def execute(self, query: str):
        if not self.connection:
            raise DatabaseClientException("There is not an active connection!")

        try:
            if not self.cursor:
                self.cursor = self.connection.cursor()

            return self.cursor.execute(query)

        except Exception as error:
            raise DatabaseClientException(error)

    def fetch_all(self) -> Iterator[Dict[str, Any]]:
        """
        Because the fetchall operation returns a list of tuples (no headers), you can use
        this function to retrieve the data in the form of dictionary...
        """

        headers = [x[0] for x in self.cursor.description]
        for row in self.cursor.fetchall():
            yield dict(zip(headers, row))

    @classmethod
    def get_create_ddl(
            cls, table_fqn: str, columns: List[Tuple[str, str]],
            temporal: bool = False) -> str:

        """
        Returns the SQL statement to create a table...

        :param table_fqn    -- Table's full qualifier name.
        :param columns      -- List of tuples defining the name and data type for the attribute...
        :param temporal     -- Defines if is a temporal table.

        :return: The query statement.
        """

        columns_def = ", ".join([
            f"{name} {cls.type_mapper.get(type_, 'VARCHAR')}" for name, type_ in columns
        ])

        return f"CREATE{' TEMPORARY' if temporal else ''} TABLE {table_fqn} ({columns_def});"

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

        if records:
            try:
                total = 0
                for chunk_ in get_batches(records, records_per_request):
                    query = self.get_insert_dml(table_fqn, columns, chunk_)
                    res = self.execute(query)
                    total += res.fetchone()[0]

                return total

            except Exception as error:
                raise DatabaseClientException(error)

    @staticmethod
    def get_insert_dml(table_fqn: str, columns: List, records: List[Dict]) -> str:
        """
        Create the query for the INSERT statement.

        :param table_fqn: Table's fully qualified name (FQN).
        :param columns: List of columns.
        :param records: List of records.
        :return: Query.
        """

        if not records:
            return ""

        values = []
        for record in records:
            tmp = [json.dumps(record[key]).replace('"', "'") for key in columns]
            values.append(f"({', '.join(tmp)})")

        return f"""INSERT INTO {table_fqn} ({', '.join(columns)}) VALUES {', '.join(values)};"""

    def delete(self, table_fqn: str, records: List[Dict], column_id: str, timestamp_col: str):
        """ Delete records """

        if not records:
            return

        query = self.get_delete_dml(
            table_fqn=table_fqn, records=records, column_id=column_id,
            timestamp_col=timestamp_col)

        self.execute(query)
        self.connection.commit()

    @staticmethod
    def get_delete_dml(
            table_fqn: str, records: List[Dict], column_id: str = None,
            timestamp_col: str = None) -> str:

        """ Creates the DELETE statement """

        if column_id:
            in_statement = ", ".join([f"{json.dumps(rec[column_id])}" for rec in records])

            return f"DELETE FROM {table_fqn} " \
                   f"WHERE {column_id} " \
                   f"IN ({in_statement});".replace('"', "'")

        statements = []
        for record in records:
            statements.append(
                " AND ".join([
                    f"{key} = '{record[key]}'"
                    for key in records[0].keys() if key != timestamp_col
                ])
            )

        return f"DELETE FROM {table_fqn} WHERE {' OR '.join([f'({sts})' for sts in statements])};"

    def close(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()
