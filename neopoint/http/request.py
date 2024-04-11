import json
from functools import cached_property
from types import MappingProxyType
from typing import Any

from ..wsgi import WSGIEnvironmentDTO
from .exceptions import RequestInvalidContentTypeError
from .message import Message
from .path_params import PathParams
from .query_params import QueryParams
from .request_method import RequestMethod

__all__ = [
    "Request",
]


class Request(Message):
    _method: RequestMethod
    _path: str
    _query_params: QueryParams
    _path_params: PathParams

    def __init__(self, wsgi_environ: WSGIEnvironmentDTO, path_params: PathParams) -> None:
        self._path = wsgi_environ.path_info
        self._query_params = QueryParams(wsgi_environ.query_string)
        self._method = wsgi_environ.request_method
        self._path_params = path_params

        super().__init__(
            content=wsgi_environ.wsgi_input.read(wsgi_environ.content_length),
            headers=wsgi_environ.http_header,
            media_type=wsgi_environ.content_type,
        )

    @property
    def headers(self) -> MappingProxyType[str, str]:
        return MappingProxyType(self._headers)

    @property
    def query_params(self) -> QueryParams:
        return self._query_params

    @property
    def path_params(self) -> PathParams:
        return self._path_params

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def path(self) -> str:
        return self._path

    @cached_property
    def json(self) -> Any:
        if self.media_type != "application/json":
            raise RequestInvalidContentTypeError(
                f"Error: trying get json from request which has non json content-type '{self.media_type}'\n"
            )
        return json.loads(self._content)
