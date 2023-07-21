import json
from functools import cached_property
from types import MappingProxyType
from typing import Any

from ..wsgi import WsgiEnviron
from .request_method import RequestMethod

__all__ = ("Request",)


class RequestInvalidContentTypeError(Exception):
    ...


class Request:
    _header: MappingProxyType[str, Any]
    _method: RequestMethod
    _content_type: str
    _content_length: int
    _path: str
    _content: bytes

    def __init__(self, wsgi_environ: WsgiEnviron) -> None:
        self._header = wsgi_environ.http_header.items().mapping
        self._method = wsgi_environ.request_method
        self._content_type = wsgi_environ.content_type
        self._content_length = wsgi_environ.content_length
        self._path = wsgi_environ.path_info
        self._content = wsgi_environ.wsgi_input.read(self.content_length)

    @property
    def header(self) -> MappingProxyType[str, str]:
        return self._header

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def content_length(self) -> int:
        return self._content_length

    @property
    def path(self) -> str:
        return self._path

    @cached_property
    def json(self) -> dict[Any, Any]:
        if self.content_type != "application/json":
            raise RequestInvalidContentTypeError(
                f"Error: trying get json from request which has non json content-type '{self.content_type}'\n"
            )
        return json.loads(self._content)
