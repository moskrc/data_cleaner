from abc import ABC, abstractmethod
from functools import wraps
from typing import Optional, Union

from html_sanitizer import Sanitizer


class BaseSanitizer(ABC):
    @abstractmethod
    def sanitize(self, s: str) -> str:
        ...

class HtmlSanitizer(BaseSanitizer):
    def __init__(self):
        self.sanitizer = Sanitizer()

    def sanitize(self, s: str) -> str:
        return self.sanitizer.sanitize(s)


class DataSanitizer:
    def __init__(self, sanitizer: BaseSanitizer):
        self.sanitizer = sanitizer

    def clean(self, data: Union[str, dict]) -> Union[str, dict]:
        if isinstance(data, dict):
            new_dict = {}
            for key, value in data.items():
                new_dict[key] = self.clean(value)
            return new_dict
        elif isinstance(data, list):
            new_list = []
            for item in data:
                new_list.append(self.clean(item))
            return new_list
        elif isinstance(data, str):
            return self.sanitizer.sanitize(data)
        else:
            return data


def sanitize_kwargs(items: Optional[Union[list[str], str]] = None):
    data_sanitizer = DataSanitizer(HtmlSanitizer())

    if isinstance(items, str):
        items = [items]
    if not items:
        items = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            modified_kwargs = dict(
                (k, data_sanitizer.clean(v) if k in items or not items else v) for k, v in kwargs.items()
            )
            return func(*args, **modified_kwargs)

        return wrapper

    return decorator
