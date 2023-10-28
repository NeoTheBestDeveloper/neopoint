import re
from typing import Any, Callable, TypeAlias

from ..http import Request, RequestMethod, Response

__all__ = [
    "Controller",
    "Url",
]

Controller: TypeAlias = Callable[[Any], Response]


class Url:
    _path_re_pattern: re.Pattern
    _path_pattern: str
    _method: RequestMethod
    _controller: Controller

    def __init__(self, path_pattern: str, method: RequestMethod, controller: Controller) -> None:
        self._method = method
        self._controller = controller
        self._path_re_pattern = self._get_re_pattern(path_pattern)
        self._path_pattern = path_pattern

    def _get_re_pattern(self, path_pattern: str) -> re.Pattern:
        while "{" in path_pattern and "}" in path_pattern:
            reg_start = path_pattern.find("{")
            reg_end = path_pattern.find("}") + 1

            path_pattern = path_pattern[:reg_start] + r"(.+)" + path_pattern[reg_end:]

        return re.compile(path_pattern)

    def match_by_path(self, path: str) -> bool:
        return self._path_re_pattern.fullmatch(path) is not None

    def match_by_method(self, method: RequestMethod) -> bool:
        return self._method == method

    def handle_request(self, request: Request) -> Response:
        return self._controller(request)

    def append_prefix(self, prefix: str) -> None:
        self._path_pattern = prefix + self._path_pattern
        self._path_re_pattern = re.compile(prefix + self._path_re_pattern.pattern)

    @property
    def controller(self) -> Controller:
        return self._controller

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def path_pattern(self) -> str:
        return self._path_pattern

    @property
    def path_re_pattern(self) -> re.Pattern:
        return self._path_re_pattern
