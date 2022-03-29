# encoding: utf-8

import logging
import sqlparse
from databricks import sql as dbsql

from dbsqlcli.packages import special
from dbsqlcli.packages.format_utils import format_status

logger = logging.getLogger(__name__)


class SQLExecute(object):
    DATABASES_QUERY = "SHOW DATABASES"

    def __init__(self, hostname, http_path, access_token, database):
        self.hostname = hostname
        self.http_path = http_path
        self.access_token = access_token
        self.database = database

        self.connect()

    def connect(self, database=None):
        conn = dbsql.connect(
            server_hostname=self.hostname,
            http_path=self.http_path,
            access_token=self.access_token,
            schema=database or 'default'
        )

        self.database = database or self.database

        if hasattr(self, "conn"):
            self.conn.close()
        self.conn = conn

    def run(self, statement):
        """Execute the sql in the database and return the results.

        The results are a list of tuples. Each tuple has 4 values
        (title, rows, headers, status).
        """
        # Remove spaces and EOL

        statement = statement.strip()
        if not statement:  # Empty string
            yield (None, None, None, None)

        # Split the sql into separate queries and run each one.
        components = sqlparse.split(statement)

        for sql in components:
            # Remove spaces, eol and semi-colons.
            sql = sql.rstrip(";")

            # \G is treated specially since we have to set the expanded output.
            if sql.endswith("\\G"):
                special.set_expanded_output(True)
                sql = sql[:-2].strip()

            with self.conn.cursor() as cur:

                try:
                    for result in special.execute(cur, sql):
                        yield result
                except special.CommandNotFound:  # Regular SQL
                    cur.execute(sql)
                    yield self.get_result(cur)

    def get_result(self, cursor):
        """Get the current result's data from the cursor."""
        title = headers = None

        # cursor.description is not None for queries that return result sets,
        # e.g. SELECT or SHOW.
        if cursor.description is not None:
            headers = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            status = format_status(rows_length=len(rows), cursor=cursor)
        else:
            logger.debug("No rows in result.")
            rows = None
            status = format_status(rows_length=None, cursor=cursor)
        return (title, rows, headers, status)


    def tables(self):
        """Yields table names."""

        TABLE_NAME = 2
        with self.conn.cursor() as cur:
            data = cur.tables(schema_name=self.database).fetchall()
            _tables = [i[TABLE_NAME] for i in data]

        for row in _tables:
            yield (row,)

    def table_columns(self, tables):
        """Yields column names."""

        TABLE_NAME = 2
        COLUMN_NAME = 3

        _all_tables = [i for i in self.tables()]

        with self.conn.cursor() as cur:
            if len(_all_tables) < 100:
                data = cur.columns(schema_name=self.database).fetchall()
                _columns = [(i[TABLE_NAME], i[COLUMN_NAME]) for i in data]
            else:
                _columns = []
                for table in tables:
                    data = cur.columns(schema_name=self.database, table_name=table).fetchall()
                    _transformed = [(i[TABLE_NAME], i[COLUMN_NAME]) for i in data]
                    _columns.extend(_transformed)

        for row in _columns:
            if row[0] in tables:
                yield row[0], row[1]

    def databases(self):
        with self.conn.cursor() as cur:
            _databases = cur.schemas().fetchall()
            return [x[0] for x in _databases]
