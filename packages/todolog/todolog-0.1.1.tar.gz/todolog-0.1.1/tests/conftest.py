import inspect
import os

import pytest

from todolog.parser import TOMLParser


def get_caller_dir():
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame[0])
    caller_dir = os.path.abspath(caller_module.__file__)
    return caller_dir


@pytest.fixture(scope="function")
def toml_parser():
    yield TOMLParser(caller_dir=get_caller_dir())
    TOMLParser.cleanup()
