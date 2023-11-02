from typing import Callable, TypeAlias

from neopoint.http.path_pattern import PathPattern
from neopoint.http.request_method import RequestMethod
from neopoint.http.response import Response

__all__ = [
    "Controller",
    "Path",
]

Controller: TypeAlias = Callable[..., Response]


class Path:
    _pattern: PathPattern
    _method: RequestMethod
    _controller: Controller

    def __init__(self, syntax_pattern: str, method: RequestMethod, controller: Controller) -> None:
        self._method = method
        self._controller = controller
        self._pattern = PathPattern(syntax_pattern)

    def match_by_path(self, path: str) -> bool:
        return self._pattern.match(path) is not None

    def match_by_method(self, method: RequestMethod) -> bool:
        return self._method == method

    def append_prefix(self, prefix: str) -> None:
        self._pattern.append_prefix(prefix)

    @property
    def controller(self) -> Controller:
        return self._controller

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def pattern(self) -> PathPattern:
        return self._pattern
