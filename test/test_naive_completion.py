import pytest
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document


@pytest.fixture
def completer():
    import dbsqlcli.completer as sqlcompleter

    return sqlcompleter.DBSQLCompleter(smart_completion=False)


@pytest.fixture
def complete_event():
    from unittest.mock import Mock

    return Mock()


def test_empty_string_completion(completer, complete_event):
    text = ""
    position = 0
    result = completer.get_completions(
        Document(text=text, cursor_position=position), complete_event
    )
    assert result == list(map(Completion, sorted(completer.all_completions)))


def test_select_keyword_completion(completer, complete_event):
    text = "SEL"
    position = len("SEL")
    result = completer.get_completions(
        Document(text=text, cursor_position=position), complete_event
    )
    assert result == list([Completion(text="SELECT", start_position=-3)])


def test_function_name_completion(completer, complete_event):
    text = "select map_con"
    position = len("select map_con")
    result = completer.get_completions(
        Document(text=text, cursor_position=position), complete_event
    )

    assert result == [
        Completion(text="map_concat", start_position=-7),
        Completion(text="map_contains_key", start_position=-7),
    ]


def test_column_name_completion(completer, complete_event):
    text = "SELECT  FROM users"
    position = len("SELECT ")
    result = completer.get_completions(
        Document(text=text, cursor_position=position), complete_event
    )
    assert result == list(map(Completion, sorted(completer.all_completions)))


def test_various_join_completions(completer, complete_event):
    for join_type in ["INNER", "OUTER", "CROSS", "LEFT", "RIGHT", "FULL"]:
        text = "SELECT foo FROM bar " + join_type + " "
        position = len(text)
        result = completer.get_completions(
            Document(text=text, cursor_position=position),
            complete_event,
            smart_completion=True,
        )
        assert Completion(text="JOIN") in result


def test_outer_join_completion(completer, complete_event):
    for join_type in ["LEFT", "RIGHT", "FULL"]:
        text = "SELECT foo FROM bar " + join_type + " "
        position = len(text)
        result = completer.get_completions(
            Document(text=text, cursor_position=position),
            complete_event,
            smart_completion=True,
        )
        assert Completion(text="OUTER JOIN") in result
