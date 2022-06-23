from dbsqlcli.completer import DBSQLCompleter
from dbsqlcli.packages.completion_engine import Table


class FakeDocument:
    def __init__(self, text, text_before_cursor):
        self.text = text
        self.text_before_cursor = text_before_cursor

    def get_word_before_cursor(self, *args, **kwargs):
        return self.text_before_cursor


def test_completer():
    completer = DBSQLCompleter()

    document = FakeDocument("create table default.", "create table default.")

    try:
        completer.get_completions(document, None)
    except Exception:
        assert False, "get_compeltions shouldn't raise"
