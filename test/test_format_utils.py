# -*- coding: utf-8 -*-


from collections import namedtuple
from dbsqlcli.packages.format_utils import format_status, humanize_size


def test_format_status_plural():
    assert format_status(rows_length=1) == "1 row in set"
    assert format_status(rows_length=2) == "2 rows in set"


def test_format_status_no_results():
    assert format_status(rows_length=None) == "Query OK"


def test_humanize_size():
    assert humanize_size(20) == "20 B"
    assert humanize_size(2000) == "1.95 KB"
    assert humanize_size(200000) == "195.31 KB"
    assert humanize_size(20000000) == "19.07 MB"
    assert humanize_size(200000000000) == "186.26 GB"
