# -*- coding: utf-8 -*-

import oracledb

from core_db.interfaces.sql_based import SqlDatabaseClient


class OracleClient(SqlDatabaseClient):
    """
    Client for Oracle connection...

    Example #1:
    ---------------------------------------------------------------------------------------

        client = OracleClient(
            user="",
            password="",
            dsn=f"{host}:{port}/{service_name}")

        client.connect()
        res = client.execute("SELECT * FROM ...")

        for x in client.fetch_all():
            print(x)

        client.close()


    Example #2:
    ---------------------------------------------------------------------------------------

        with OracleClient(
            user="",
            password="",
            dsn=f"{host}:{port}/{service_name}") as client:

            res = client.execute("SELECT * FROM ...")
            for x in client.fetch_all():
                print(x)
    """

    def __init__(self, **kwargs):
        """
        Expected -> user, password, dsn...

        More information:
          - https://oracle.github.io/python-oracledb/
          - https://python-oracledb.readthedocs.io/en/latest/index.html

        """

        super(OracleClient, self).__init__(**kwargs)
        self.connect_fcn = oracledb.connect

    def test_connection(self, query: str = None):
        if not query:
            query = 'SELECT * FROM "V$VERSION"'

        return super(OracleClient, self).test_connection(query)
