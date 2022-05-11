# Introduction

Databricks SQL CLI is a command line interface (CLI) for [Databricks SQL](https://databricks.com/product/databricks-sql) that can do auto-completion and syntax highlighting, and is a proud member of the dbcli community.

![](https://github.com/databricks/databricks-sql-cli/raw/main/dbsqlcli-demo.gif?raw=True)

# Quick Start

### Install via `pip`

You'll need Python 3.7 or newer.

```bash
python3 -m pip install dbsqlcli
```

You can now run `dbsqlcli` from your terminal.

## Authentication

To connect with SQL Endpoints `dbsqlcli` needs the host name and http path from the [connection details](https://docs.databricks.com/integrations/bi/jdbc-odbc-bi.html#get-connection-details-for-a-sql-endpoint) screen in Databricks SQL and a [personal access token](https://docs.databricks.com/dev-tools/api/latest/authentication.html#token-management). These can be passed in as arguments to `dbsqlcli` or by environment variables.

## Config

A config file is automatically created at `~/.dbsqlcli/dbsqlclirc` at first launch (run `dbsqlcli`). See the file itself for a description of all available options. Most users will not need to modify this file.


## Run a query

``` bash
$ dbsqlcli -e 'select id, name from minifigs LIMIT 10'
```

## Run a .sql file

```bash
$ dbsqlcli -e query.sql
```

## Run a .sql file and save to CSV

```bash
$ dbsqlcli -e query.sql > output.csv
```

## REPL

``` bash
$ cd <directory containing dbsqlcli binary>
$ ./dbslqcli [<database_name>]
```

Run the `help;` command to see a list of shortcuts

# Features

- Auto-completes as you type for SQL keywords as well as tables and columns in the database.
- Syntax highlighting.
- Smart-completion will suggest context-sensitive completion.
    - `SELECT * FROM <tab>` will only show table names.
    - `SELECT * FROM users WHERE <tab>` will only show column names.
- Pretty prints tabular data and various table formats.
- Some special commands. e.g. Favorite queries.
- Alias support. Column completions will work even when table names are aliased.

# Usages

```bash
$ dbsqlcli --help
Usage: dbsqlcli [OPTIONS] [DATABASE]

  A DBSQL terminal querying client with auto-completion and syntax
  highlighting.

  Examples:
    - dbsqlcli
    - dbsqlcli my_database

Options:
  -e, --execute TEXT   Execute a command (or a file) and quit.
  --hostname TEXT      Hostname  [env var: DBSQLCLI_HOST_NAME]
  --http-path TEXT     HTTP Path  [env var: DBSQLCLI_HTTP_PATH]
  --access-token TEXT  Access Token  [env var: DBSQLCLI_ACCESS_TOKEN]
  --clirc FILE         Location of clirc file.
  --table-format TEXT  Table format used with -e option.
  --help               Show this message and exit.
```


# Contributions

During its internal release, please report issues in the #dbsqlcli Slack channel.

We use [Poetry](https://python-poetry.org/docs/) for development. Follow the instructions to install Poetry on your system. 

1. Clone this repository
2. `poetry install` will install its dependencies
3. `poetry shell` will activate the local virtual environment
4. `python app.py` will run `dbsqlcli` incorporating any of your local changes

# Credits

Huge thanks to the maintainers of https://github.com/dbcli/athenacli upon which this project is built.

# Similar projects

The [DBCLI](https://github.com/dbcli) organization on Github maintains CLIs for numerous database platforms including MySQL, Postgres, and MSSQL. 

- https://github.com/dbcli/mycli
- https://github.com/dbcli/pgcli
- https://github.com/dbcli/mssql-cli

