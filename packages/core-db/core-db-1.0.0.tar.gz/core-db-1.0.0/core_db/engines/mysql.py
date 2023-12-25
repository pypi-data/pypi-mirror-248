# -*- coding: utf-8 -*-

import json
from typing import List, Dict

import pymysql

from core_db.interfaces.sql_based import SqlDatabaseClient


class MySQLClient(SqlDatabaseClient):
    """
    Client for MySQL connection...

    Example #1:
    ---------------------------------------------------------------------------------------

        client = MySQLClient(
            host="localhost",
            user="root",
            password="SomePassword")

        client.connect()
        res = client.execute("SELECT * FROM ...;")

        for x in client.fetch_all():
            print(x)

        client.close()

    Example #2:
    ---------------------------------------------------------------------------------------

        with MySQLClient(
            host="localhost",
            user="root",
            password="SomePassword") as client:

            client.execute("SELECT * FROM ...;")
            for x in client.fetch_all():
                print(x)
    """

    type_mapper = {
        int: "INTEGER",
        float: "DOUBLE",
        str: "TEXT",
        bool: "BOOLEAN",
        dict: "JSON",
        list: "JSON"
    }

    def __init__(self, **kwargs):
        """
        Expected -> host, user, password, database
        More information:
          - https://pymysql.readthedocs.io/en/latest/user/index.html#
          - https://pypi.org/project/PyMySQL/
        """

        super(MySQLClient, self).__init__(**kwargs)
        self.connect_fcn = pymysql.connect
        self.epoch_to_timestamp_fcn = "FROM_UNIXTIME"

    def test_connection(self, query: str = None):
        if not query:
            query = "SELECT version();"

        return super(MySQLClient, self).test_connection(query)

    def merge(self, table_fqn: str, records: List[Dict],
              id_columns: List[str], epoch_column: str):

        """ Insert/Update process """

        if not records:
            return

        ddl = self.get_merge_dml(table_fqn, records, list(records[0].keys()), epoch_column)
        res = self.execute(ddl)
        self.connection.commit()
        return res

    @staticmethod
    def get_merge_dml(table_fqn: str, records: List[Dict], columns: List[str],
                      epoch_column: str) -> str:

        # Because the column must be at the end...
        columns.remove(epoch_column)
        columns.append(epoch_column)

        rows, recs = [[rec[key] for key in columns] for rec in records], []
        schema, table = table_fqn.split(".")

        for row in rows:
            iter_ = [
                f"'{attr}'" if isinstance(attr, str)
                else f"'{json.dumps(attr)}'" if isinstance(attr, list) or isinstance(attr, dict)
                else str(attr) for attr in row
            ]

            recs.append(f"({', '.join(iter_)})")

        return f"INSERT INTO `{schema}`.`{table}` " \
               f"({', '.join([f'`{x}`' for x in columns])}) VALUES " \
               f"{', '.join(recs)} " \
               f"ON DUPLICATE KEY UPDATE " \
               f"{', '.join([f'{y}=if(values({epoch_column}) > {epoch_column}, values({y}), {y})' for y in columns])};"
