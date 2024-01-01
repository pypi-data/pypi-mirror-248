import inspect
import logging
import datetime
import os

from typing import Callable

from .parser import TOMLParser


def todo(key: str, ignore: bool = False):
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame[0])
    caller_dir = os.path.abspath(caller_module.__file__)

    def decorator(func):
        def wrapper(*args, **kwargs):
            if ignore:
                return

            parser: TOMLParser = TOMLParser(caller_dir=caller_dir)
            values: dict = parser.get_todolog_values_by_key(key=key)

            message: str = values["message"]
            log_level: str = values["log_level"]
            due: datetime.date | None = values["due"]

            if not due or (due and due < datetime.date.today()):
                logger = logging.getLogger(__name__)
                log_handler: Callable = getattr(logger, log_level)
                log_handler(msg=message)

            return func(*args, **kwargs)
        return wrapper
    return decorator
