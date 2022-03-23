# encoding: utf-8

import logging
import sqlparse
from databricks import sql as dbsql

from dbsqlcli.packages import special
from dbsqlcli.packages.format_utils import format_status

logger = logging.getLogger(__name__)


class SQLExecute(object):
    DATABASES_QUERY = "SHOW DATABASES"
    TABLES_QUERY = "SHOW TABLES"
    TABLE_COLUMNS_QUERY = """
        show columns in default.aaron_test
    """

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

    def _load_table_and_columns(self):
        """Load tables and columns from SQL Endpoint

        Makes a call to cursor.columns() which returns both tables and columns
        """
        print("Fetching all tables and columns")
        TABLE_NAME = 2
        COLUMN_NAME = 3

        with self.conn.cursor() as cur:
            data = cur.columns(schema_name=self.database).fetchall()
            self._tables = {i[TABLE_NAME]: None for i in data}.keys()
            self._columns = [(i[TABLE_NAME], i[COLUMN_NAME]) for i in data]
    def tables(self):
        """Yields table names."""
        print("running tables")
        if not hasattr(self, "_tables"):
            self._load_table_and_columns()
        for row in self._tables:
            print(f"yielding table {row}")
            yield (row,)

    def table_columns(self, tables):
        """Yields column names."""

        # Can we ignore the tables parameter completely?
        if not hasattr(self, "_columns"):
            self._load_table_and_columns()
        
        for row in self._columns:
            if row[0] in tables:
                yield row[0], row[1]


    def databases(self):
        with self.conn.cursor() as cur:
            cur.execute(self.DATABASES_QUERY)
            return [x[0] for x in cur.fetchall()]
