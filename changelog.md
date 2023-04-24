# Release History

## 0.4.0 (unreleased)


## 0.3.1 (2023-04-24)

- Fix: Fixed sqlparse import to work regardless how sqlparse is installed

## 0.3.0 (2023-03-31)

- Removes `\u` command because it broke usages of `USE CATALOG <catalog name>`
- Fix: destructive_warning setting is now properly read from clirc file and CLI args
## 0.2.0 (2023-03-15)

- Support oauth authentication for AWS

## 0.1.4 (2022-07-01)

- Fixes to autocomplete behaviour
## 0.1.3 (2022-05-12)

- Adjustments to README

## 0.1.2 (2022-05-11)

- Allow users to read credentials from the dbsqlclirc file
- Updated list of literals used for autocomplete.
- Updated README with better usage instructions
- Changed pypi package name to databricks-sql-cli. The tool can be invoked with either dbsqlcli or databricks-sql-cli
- Removed the download command which was a holdover from pyathena