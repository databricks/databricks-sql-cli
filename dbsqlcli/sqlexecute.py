# encoding: utf-8
from typing import Optional
import logging
import sqlparse, click
from databricks import sql as dbsql

from dbsqlcli.packages import special
from dbsqlcli.packages.format_utils import format_status
from databricks.sql.exc import RequestError

from databricks.sql.experimental.oauth_persistence import OAuthPersistence, OAuthToken
from databricks.sql.auth.auth import AuthType

logger = logging.getLogger(__name__)

from dbsqlcli import __version__ as CURRENT_VERSION

USER_AGENT_STRING = f"DBSQLCLI/{CURRENT_VERSION}"

DBSQL_CLI_OAUTH_CLIENT_ID = "databricks-cli"
DBSQL_CLI_OAUTH_PORT = 8020


class OAuthPersistenceCache(OAuthPersistence):
    def __init__(self):
        self.tokens = {}

    def persist(self, hostname: str, oauth_token: OAuthToken):
        self.tokens[hostname] = oauth_token

    def read(self, hostname: str) -> Optional[OAuthToken]:
        return self.tokens.get(hostname)


oauth_token_cache = OAuthPersistenceCache()


class SQLExecute(object):
    DATABASES_QUERY = "SHOW DATABASES"

    def __init__(self, hostname, http_path, access_token, database= "default", auth_type=None):
        self.hostname = hostname
        self.http_path = http_path
        self.access_token = access_token
        self.auth_type = auth_type
        self._set_catalog_database(database)
        self.connect()

    def _set_catalog_database(self, database):
        """Sets the catalog and database name if a single dot is supplied"""
        if database.count(".") == 1:
            component = database.split(".")
            self.catalog = component[0]
            self.database = component[1]
        else:
            self.catalog = "hive_metastore"
            self.database = database

    def connect(self, database=None):
        self.close_connection()

        if database:
            self._set_catalog_database(database)

        oauth_params = {}
        if self.auth_type == AuthType.DATABRICKS_OAUTH.value:
            oauth_params = {
                "auth_type": self.auth_type,
                "experimental_oauth_persistence": oauth_token_cache,
                "oauth_client_id": DBSQL_CLI_OAUTH_CLIENT_ID,
                "oauth_redirect_port": DBSQL_CLI_OAUTH_PORT,
            }

        conn = dbsql.connect(
            server_hostname=self.hostname,
            http_path=self.http_path,
            access_token=self.access_token,
            catalog=self.catalog,
            schema=self.database,
            _user_agent_entry=USER_AGENT_STRING,
            **oauth_params,
        )

        self.conn = conn

    def close_connection(self):
        """Close any open connection and remove the `conn` attribute"""

        if not hasattr(self, "conn"):
            return

        try:
            self.conn.close()
        except AttributeError as e:
            logger.debug("There is no active connection to close.")
            delattr(self, "conn")
        except RequestError as e:
            message = "The connection is no longer active and will be recycled. It was probably was timed-out by SQL gateway"
            click.echo(message)
            logger.debug(f"{message}: {e}")
        finally:
            delattr(self, "conn")

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

            attempts = 0
            while attempts in [0, 1]:
                with self.conn.cursor() as cur:
                    try:
                        try:
                            for result in special.execute(cur, sql):
                                yield result
                            break
                        except special.CommandNotFound:  # Regular SQL
                            cur.execute(sql)
                            yield self.get_result(cur)
                            break
                    except EOFError as e:  # User enters `exit`
                        raise e
                    except RequestError as e:
                        logger.error(
                            f"SQL Gateway was timed out. Attempting to reconnect. Attempt {attempts+1}. Error: {e}"
                        )
                        attempts += 1
                        self.connect()

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
                    try:
                        data = cur.columns(
                            schema_name=self.database, table_name=table
                        ).fetchall()
                        _transformed = [(i[TABLE_NAME], i[COLUMN_NAME]) for i in data]
                        _columns.extend(_transformed)
                    except Exception as e:
                        logger.debug(f"Error fetching columns for {table}: {e}")

        for row in _columns:
            if row[0] in tables:
                yield row[0], row[1]

    def databases(self):
        with self.conn.cursor() as cur:
            _databases = cur.schemas().fetchall()
            return [x[0] for x in _databases]
