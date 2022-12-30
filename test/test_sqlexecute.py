import unittest
from unittest.mock import MagicMock, patch

import databricks
from databricks.sql.auth.auth import AuthType
from dbsqlcli.sqlexecute import (
    SQLExecute,
    DBSQL_CLI_OAUTH_CLIENT_ID,
    DBSQL_CLI_OAUTH_PORT,
)

HTTP_PATH = "arg/path/to/endpoint"
HOST_NAME = "arg.cloud.databricks.com"
ACCESS_TOKEN = "dapi_argRandomAccessKey"


class SQLExecuteTests(unittest.TestCase):
    @patch("databricks.sql.connect")
    def test_connect_with_token(self, mock_connect):
        dummy_conn = MagicMock()
        mock_connect.return_value = dummy_conn
        executor = SQLExecute(
            hostname=HOST_NAME,
            http_path=HTTP_PATH,
            access_token=ACCESS_TOKEN,
            database="default",
        )

        assert executor.conn == dummy_conn

        args, kwargs = mock_connect.call_args
        assert kwargs.get("server_hostname") == HOST_NAME
        assert kwargs.get("access_token") == ACCESS_TOKEN

    @patch("databricks.sql.connect")
    def test_connect_with_oauth(self, mock_connect):
        dummy_conn = MagicMock()
        mock_connect.return_value = dummy_conn
        executor = SQLExecute(
            hostname=HOST_NAME,
            http_path=HTTP_PATH,
            access_token="",
            database="default",
            auth_type=AuthType.DATABRICKS_OAUTH.value,
        )

        assert executor.conn == dummy_conn

        args, kwargs = mock_connect.call_args
        assert kwargs.get("server_hostname") == HOST_NAME
        assert kwargs.get("auth_type") == AuthType.DATABRICKS_OAUTH.value
        assert kwargs.get("oauth_client_id") == DBSQL_CLI_OAUTH_CLIENT_ID
        assert kwargs.get("oauth_redirect_port") == DBSQL_CLI_OAUTH_PORT
