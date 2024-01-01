import os
import threading
import datetime
from functools import cache

import tomli


def singleton_with_argument(cls):
    instances = {}
    lock = threading.Lock()

    def wrapper(*args, **kwargs):
        key = (cls, args, frozenset(kwargs.items()))
        with lock:
            if key not in instances:
                instances[key] = cls(*args, **kwargs)
            return instances[key]

    def cleanup():
        nonlocal instances
        instances = {}

    wrapper.cleanup = cleanup
    return wrapper


@singleton_with_argument
class TOMLParser:
    def __init__(self, caller_dir: str):
        self.caller_dir = caller_dir
        self._load_todolog_toml_values = cache(self.__load_todolog_toml_values)
        self.get_todolog_values_by_key = cache(self.__get_todolog_values_by_key)
        self.todolog_filename = self._load_todolog_filename()
        self.default_log_message = self._load_todolog_default_log_message()

    def __get_todolog_values_by_key(self, key: str) -> dict:
        todolog_path: str | None = self._find_path_recursively(filename=self.todolog_filename)
        todolog_toml_values: dict = self._load_toml(path=todolog_path)

        values: dict = todolog_toml_values.get(key)
        if not values:
            raise KeyError("Invalid todolog key: " + key)

        message: str | None = values.get("message", self.default_log_message)
        due: datetime.date | None = values.get("due")

        if due and not isinstance(due, datetime.date):
            raise ValueError("due can only be specified by date.")

        log_level: str = values.get("log_level", "INFO").lower()

        if log_level not in ("debug", "info", "warning", "error", "critical"):
            raise ValueError("Invalid log_level: " + log_level)

        return {"message": message, "due": due, "log_level": log_level}

    def _load_todolog_filename(self) -> str:
        todolog_toml_values: dict = self._load_todolog_toml_values()
        todolog_filename: str | None = todolog_toml_values.get("filename")
        return self._validate_todolog_filename(filename=todolog_filename)

    def _load_todolog_default_log_message(self) -> str:
        todolog_toml_values: dict = self._load_todolog_toml_values()
        default_log_message: str = todolog_toml_values.get("default_log_message", "Found ToDo")
        return default_log_message

    def __load_todolog_toml_values(self) -> dict:
        pyproject_toml_path: str | None = self._find_path_recursively(filename="pyproject.toml")

        if pyproject_toml_path is None:
            raise FileNotFoundError("pyproject.toml Not Found.")

        pyproject_toml_values: dict = self._load_toml(path=pyproject_toml_path)
        return pyproject_toml_values.get("tool", {}).get("todolog", {})

    @staticmethod
    def _load_toml(path: str) -> dict:
        with open(path, "rb") as f:
            return tomli.load(f)

    @staticmethod
    def _validate_todolog_filename(filename: str | None) -> str:
        if not filename:
            raise ValueError("tool.todolog.filename Not Found.")

        if not isinstance(filename, str):
            raise TypeError("filename must be str.")

        if len(filename.split(".")) < 2:
            raise ValueError("Invalid filename.")

        if not filename.endswith(".toml"):
            raise ValueError("Invalid filename. Filename must be endswith `.toml`.")

        return filename

    def _find_path_recursively(self, filename: str) -> str | None:
        current_dir: str = self.caller_dir

        while True:
            file_path: str = os.path.join(current_dir, filename)

            if os.path.isfile(file_path):
                return file_path

            if current_dir == os.path.dirname(current_dir):
                break

            current_dir = os.path.dirname(current_dir)
