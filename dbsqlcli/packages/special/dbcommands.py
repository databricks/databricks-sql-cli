import logging
from databricks.sql import ProgrammingError

from dbsqlcli import __version__
from dbsqlcli.packages.special import iocommands
from dbsqlcli.packages.special.utils import format_uptime
from .main import special_command, RAW_QUERY, PARSED_QUERY

log = logging.getLogger(__name__)


@special_command(
    "\\dt",
    "\\dt [table]",
    "List or describe tables.",
    arg_type=PARSED_QUERY,
    case_sensitive=True,
)
def list_tables(cur, arg=None, arg_type=PARSED_QUERY, verbose=False):
    if arg:
        query = "SHOW COLUMNS FROM {0}".format(arg)
    else:
        query = "SHOW TABLES"
    log.debug(query)
    cur.execute(query)
    tables = cur.fetchall()
    status = ""
    if cur.description:
        headers = [x[0] for x in cur.description]
    else:
        return [(None, None, None, "")]

    return [(None, tables, headers, status)]


@special_command(
    "\\l", "\\l", "List databases.", arg_type=RAW_QUERY, case_sensitive=True
)
def list_databases(cur, **_):
    _databases = cur.schemas().fetchall()
    if _databases:
        headers = [x[0] for x in _databases]
        return [(None, _databases, headers, "")]
    else:
        return [(None, None, None, "")]
