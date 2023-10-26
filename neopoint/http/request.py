import json
from functools import cached_property
from typing import Any

from neopoint.http.message import Message

from ..wsgi import WSGIEnviron
from .request_method import RequestMethod

__all__ = [
    "Request",
]


class RequestInvalidContentTypeError(Exception):
    ...


class Request(Message):
    _method: RequestMethod
    _path: str

    def __init__(self, wsgi_environ: WSGIEnviron) -> None:
        self._method = wsgi_environ.request_method
        self._path = wsgi_environ.path_info

        super().__init__(
            content=wsgi_environ.wsgi_input.read(wsgi_environ.content_length),
            headers=wsgi_environ.http_header,
            media_type=wsgi_environ.content_type,
        )

    @property
    def headers(self) -> MappingProxyType[str, str]:
        return MappingProxyType(self._headers)

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def content_length(self) -> int:
        return len(self._content)

    @property
    def path(self) -> str:
        return self._path

    @cached_property
    def json(self) -> dict[Any, Any]:
        if self.media_type != "application/json":
            raise RequestInvalidContentTypeError(
                f"Error: trying get json from request which has non json content-type '{self.media_type}'\n"
            )
        return json.loads(self._content)
