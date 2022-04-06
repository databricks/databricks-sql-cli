from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import Condition
from prompt_toolkit.application import get_app


def cli_is_multiline(cli):
    @Condition
    def cond():
        doc = get_app().layout.get_buffer_by_name(DEFAULT_BUFFER).document
        if not cli.multi_line:
            return False
        else:
            return not _multiline_exception(doc.text)

    return cond


def _multiline_exception(text):
    orig = text
    text = text.strip()

    # Multi-statement favorite query is a special case. Because there will
    # be a semicolon separating statements, we can't consider semicolon an
    # EOL. Let's consider an empty line an EOL instead.
    # if text.startswith('\\fs'):
    #     return orig.endswith('\n')

    return (
        text.startswith("\\")
        or text.endswith(";")  # Special Command
        or text.endswith("\\g")  # Ended with a semi-colon
        or text.endswith("\\G")  # Ended with \g
        or (text == "exit")  # Ended with \G
        or (text == "quit")  # Exit doesn't need semi-colon
        or (text == ":q")  # Quit doesn't need semi-colon
        or (  # To all the vim fans out there
            text == ""
        )  # Just a plain enter without any text
    )
