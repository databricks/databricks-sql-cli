from dbsqlcli.main import apply_credentials_from_cfg

from databricks.sql.auth.auth import AuthType

CONFIG = {
    "credentials": {
        "http_path": "config/path/to/endpoint",
        "host_name": "config.cloud.databricks.com",
        "access_token": "dapi_configRandomAccessKey",
    }
}


HTTP_PATH = "arg/path/to/endpoint"
HOST_NAME = "arg.cloud.databricks.com"
ACCESS_TOKEN = "dapi_argRandomAccessKey"


def test_clirc_credentials_are_used():
    """When no credentials are passed to the CLI, read credentials from the config file
    """


    host_name, http_path, access_token, auth_type = apply_credentials_from_cfg(
        None, None, None, None, CONFIG
    )

    assert http_path == "config/path/to/endpoint"
    assert host_name == "config.cloud.databricks.com"
    assert access_token == "dapi_configRandomAccessKey"


def test_cli_args_credentials_are_used():
    """When credentials are passed to the CLI, use these instead of the config file.
    """


    host_name, http_path, access_token, auth_type = apply_credentials_from_cfg(
        HOST_NAME, HTTP_PATH, ACCESS_TOKEN, AuthType.DATABRICKS_OAUTH.value, CONFIG
    )

    assert http_path == HTTP_PATH
    assert host_name == HOST_NAME
    assert access_token == ACCESS_TOKEN
    assert auth_type == AuthType.DATABRICKS_OAUTH.value


def test_blended_credentials_are_used():
    """When some credentials are passed ot the CLI, use config file to fill in the gaps.
    """

    credential = CONFIG["credentials"].copy()
    credential["auth_type"] = AuthType.DATABRICKS_OAUTH.value

    host_name, http_path, access_token, auth_type = apply_credentials_from_cfg(
        hostname=None,
        http_path=HTTP_PATH,
        access_token=None,
        auth_type=None,
        cfg={"credentials": credential},
    )

    assert host_name == "config.cloud.databricks.com"
    assert http_path == HTTP_PATH
    assert access_token == "dapi_configRandomAccessKey"
    assert auth_type == AuthType.DATABRICKS_OAUTH.value
