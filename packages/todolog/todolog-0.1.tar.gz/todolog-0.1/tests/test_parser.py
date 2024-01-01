# Success
import datetime

from todolog import todo


def test_find_pyproject_toml_filename(toml_parser):
    assert toml_parser.todolog_filename == "todolog.toml"


def test_find_pyproject_toml_default_log_message(toml_parser):
    assert toml_parser.default_log_message == "default"


def test_get_todolog_values_by_key(toml_parser):
    assert toml_parser.get_todolog_values_by_key("key1") == {
        "message": "This is a log message.",
        "due": datetime.date(2023, 12, 31),
        "log_level": "warning",
    }


def test_log(caplog):

    @todo(key="key1")
    def todo_function():
        pass

    todo_function()

    assert "This is a log message." in caplog.messages


# Fail
def test_find_file(toml_parser):
    path = toml_parser._find_path_recursively(filename="invalid.toml")
    assert path is None
