# Introduction

AthenaCLI is a command line interface (CLI) for the [Athena](https://aws.amazon.com/athena/) service that can do auto-completion and syntax highlighting, and is a proud member of the dbcli community.

![](./docs/_static/gif/athenacli.gif)

# Quick Start

## Install

### Install via `pip`

TBD

### Download a release

TBD

## Config

A config file is automatically created at `~/.athenacli/athenaclirc` at first launch (run athenacli). See the file itself for a description of all available options.

Below 4 variables are required. If you are a user of aws cli, you can refer to [awsconfig](./docs/awsconfig.rst) file to see how to reuse credentials configuration of aws cli.

``` text
# AWS credentials
aws_access_key_id = ''
aws_secret_access_key = ''
region = '' # e.g us-west-2, us-east-1

# Amazon S3 staging directory where query results are stored.
# NOTE: S3 should in the same region as specified above.
# The format is 's3://<your s3 directory path>'
s3_staging_dir = ''

# Name of athena workgroup that you want to use
work_group = '' # e.g. primary
```

or you can also use environment variables:

``` bash
$ export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
$ export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
$ export AWS_DEFAULT_REGION=us-west-2
$ export AWS_ATHENA_S3_STAGING_DIR=s3://YOUR_S3_BUCKET/path/to/
$ export AWS_ATHENA_WORK_GROUP=YOUR_ATHENA_WORK_GROUP
```

## Create a table

``` bash
$ athenacli -e examples/create_table.sql
```

You can find `examples/create_table.sql` [here](./examples/create_table.sql).

## Run a query

``` bash
$ athenacli -e 'select elb_name, request_ip from elb_logs LIMIT 10'
```

## REPL

``` bash
$ athenacli [<database_name>]
```

# Features

- Auto-completes as you type for SQL keywords as well as tables and columns in the database.
- Syntax highlighting.
- Smart-completion will suggest context-sensitive completion.
    - `SELECT * FROM <tab>` will only show table names.
    - `SELECT * FROM users WHERE <tab>` will only show column names.
- Pretty prints tabular data and various table formats.
- Some special commands. e.g. Favorite queries.
- Alias support. Column completions will work even when table names are aliased.

Please refer to the [Features](./docs/features.rst) page for the screenshots of above features.

# Usages

```bash
$ athenacli --help
Usage: main.py [OPTIONS] [DATABASE]

A Athena terminal client with auto-completion and syntax highlighting.

Examples:
    - athenacli
    - athenacli my_database

Options:
-e, --execute TEXT            Execute a command (or a file) and quit.
-r, --region TEXT             AWS region.
--aws-access-key-id TEXT      AWS access key id.
--aws-secret-access-key TEXT  AWS secretaccess key.
--s3-staging-dir TEXT         Amazon S3 staging directory where query
                                results are stored.
--work-group TEXT             Amazon Athena workgroup in which query is run, default is primary
--athenaclirc PATH            Location of athenaclirc file.
--help                        Show this message and exit.
```

Please go to the [Usages](https://athenacli.readthedocs.io/en/latest/usage.html) for detailed information on how to use AthenaCLI.

# Contributions

TBD

# Credits

// Thank the athenacli guy.

# Similar projects

Link to dbcli.
