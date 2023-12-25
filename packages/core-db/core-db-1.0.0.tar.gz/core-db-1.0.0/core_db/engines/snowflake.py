# -*- coding: utf-8 -*-

import json
from random import randint
from typing import List, Dict

import snowflake.connector

from core_db.interfaces.sql_based import SqlDatabaseClient


class SnowflakeClient(SqlDatabaseClient):
    """ Client to connect to Snowflake Data Warehouse """

    type_mapper = {
        int: "INTEGER",
        float: "DOUBLE",
        str: "VARCHAR",
        bool: "BOOLEAN",
        dict: "OBJECT",
        list: "VARIANT"
    }

    def __init__(self, **kwargs):
        """
        :param kwargs:
            * user: Username.
            * host: Hostname.
            * account: Account name.
            * password: Password.
            * warehouse: Warehouse.
            * database: Database.
            * schema: Schema.
            * role: Role.

        To connect using OAuth, the connection string must include the authenticator parameter set
        to oauth and the token parameter set to the oauth_access_token.
        https://docs.snowflake.com/en/user-guide/python-connector-example.html#connecting-with-oauth

        :param authenticator="oauth"
        :param token="oauth_access_token"
        """

        super().__init__(**kwargs)
        self.connect_fcn = snowflake.connector.connect
        self.epoch_to_timestamp_fcn = "TO_TIMESTAMP"

    def test_connection(self, query: str = None):
        if not query:
            query = "SELECT current_version();"

        res = self.execute(query)
        return res.fetchone()[0]

    @staticmethod
    def get_insert_dml(table_fqn: str, columns: List, records: List[Dict]) -> str:
        if records:
            select_statement = ", ".join([
                f"PARSE_JSON(Column{pos + 1}) AS {column}"
                if isinstance(records[0][column], list) or isinstance(records[0][column], dict)
                else f"Column{pos + 1} AS {column}"
                for pos, column in enumerate(columns)
            ])

            values = []
            for record in records:
                tmp = []
                for key in columns:
                    value = record[key]

                    tmp.append(
                        f"'{json.dumps(value)}'" if isinstance(value, list) or isinstance(value, dict)
                        else f"'{value}'" if isinstance(value, str)
                        else str(value)
                    )

                values.append(f"({', '.join(tmp)})")

            return f"INSERT INTO {table_fqn} " \
                   f"SELECT {select_statement} " \
                   f"FROM VALUES {', '.join(values)};"

    def merge(self, table_fqn: str, records: List[Dict], id_columns: List[str],
              epoch_column: str):

        """ Insert/Update process """

        if not records:
            return

        columns_type, column_names = [], []
        for key, value in records[0].items():
            columns_type.append((key, type(value)))
            column_names.append(key)

        temp_table = f"{table_fqn}_{randint(1, 1000)}"
        create_ddl = self.get_create_ddl(temp_table, columns_type)
        self.execute(create_ddl)

        insert_dml = self.get_insert_dml(table_fqn, column_names, records)
        self.execute(insert_dml)

        merge_dml = self.get_merge_ddl(
            temp_table, table_fqn, id_columns,
            column_names, epoch_column)

        self.execute(merge_dml)
        self.connection.commit()

    @staticmethod
    def get_merge_ddl(target: str, source: str, columns_on: List[str],
                      columns: List[str], epoch_column: str):

        on_sts = " AND ".join([f"NVL({source}.{key}, '') = NVL({target}.{key}, '')" for key in columns_on])
        set_sts = ", ".join([f"{target}.{key} = {source}.{key}" for key in columns + [epoch_column]])
        all_columns = columns_on + columns + [epoch_column]

        return f"MERGE INTO {target} " \
               f"USING {source} " \
               f"ON {on_sts} " \
               f"WHEN matched AND {source}.{epoch_column} > {target}.{epoch_column} THEN " \
               f"UPDATE SET {set_sts} " \
               f"WHEN NOT matched THEN " \
               f"INSERT ({', '.join(all_columns)}) " \
               f"VALUES ({', '.join([f'{source}.{key}' for key in all_columns])});"
