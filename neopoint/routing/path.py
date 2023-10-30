from typing import Any, Callable, TypeAlias

from neopoint.http.path_re import PathRe
from neopoint.http.request_method import RequestMethod
from neopoint.http.response import Response

__all__ = [
    "Controller",
    "Path",
]

Controller: TypeAlias = Callable[[Any], Response]


class Path:
    _path_pattern: PathRe
    _method: RequestMethod
    _controller: Controller

    def __init__(self, path_pattern: str, method: RequestMethod, controller: Controller) -> None:
        self._method = method
        self._controller = controller
        self._path_pattern = PathRe(path_pattern)

    def match_by_path(self, path: str) -> bool:
        return self._path_pattern.match(path) is not None

    def match_by_method(self, method: RequestMethod) -> bool:
        return self._method == method

    def append_prefix(self, prefix: str) -> None:
        self._path_pattern.append_prefix(prefix)

    @property
    def controller(self) -> Controller:
        return self._controller

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def path_pattern(self) -> PathRe:
        return self._path_pattern
