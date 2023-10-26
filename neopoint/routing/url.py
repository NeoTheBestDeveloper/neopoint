import re
from typing import Any, Callable, TypeAlias

from ..http import Request, RequestMethod, Response

__all__ = [
    "Controller",
    "Url",
]

Controller: TypeAlias = Callable[[Any], Response]


class Url:
    _path: str
    _method: RequestMethod
    _controller: Controller

    def __init__(self, path: str, method: RequestMethod, controller: Controller) -> None:
        self._method = method
        self._controller = controller
        self._path = path

    def match(self, path: str, method: RequestMethod) -> bool:
        return re.match(f"^{self._path}$", path) is not None and self._method == method

    def handle_request(self, request: Request) -> Response:
        return self._controller(request)

    def append_prefix(self, prefix: str) -> None:
        self._path = prefix + self._path

    @property
    def controller(self) -> Controller:
        return self._controller

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def path(self) -> str:
        return self._path

    def __str__(self) -> str:
        return f"Url(path={self._path}, method={self._method}, controller={self._controller})"
