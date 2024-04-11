from dataclasses import dataclass
from io import BufferedReader
from typing import Literal
from wsgiref.types import WSGIEnvironment
from wsgiref.util import FileWrapper

from ..http.http_version import HttpVersion
from ..http.request_method import RequestMethod
from .exceptions import UnsupportedProtocolError
from .wsgi_version import WSGIVersion

__all__ = [
    "WSGIEnvironmentDTO",
]


# pylint: disable=too-many-instance-attributes
@dataclass(slots=True, frozen=True, match_args=False, init=False)
class WSGIEnvironmentDTO:
    wsgi_version: WSGIVersion
    wsgi_url_scheme: Literal["http", "https"]
    wsgi_input: BufferedReader
    wsgi_errors: BufferedReader
    wsgi_multithread: bool
    wsgi_multiprocess: bool
    wsgi_run_once: bool
    wsgi_file_wrapper: FileWrapper | None
    wsgi_input_terminated: bool

    request_method: RequestMethod
    script_name: str
    path_info: str
    query_string: str
    content_type: str
    content_length: int
    server_name: str
    server_port: int
    http_version: HttpVersion

    http_header: dict[str, str]

    def __init__(self, environ: WSGIEnvironment) -> None:
        # WSGI keys.
        object.__setattr__(self, "wsgi_version", WSGIVersion(*environ["wsgi.version"]))
        object.__setattr__(self, "wsgi_url_scheme", environ["wsgi.url_scheme"])
        object.__setattr__(self, "wsgi_input", environ["wsgi.input"])
        object.__setattr__(self, "wsgi_errors", environ["wsgi.errors"])
        object.__setattr__(self, "wsgi_multithread", bool(environ["wsgi.multithread"]))
        object.__setattr__(self, "wsgi_multiprocess", bool(environ["wsgi.multiprocess"]))
        object.__setattr__(self, "wsgi_run_once", bool(environ["wsgi.run_once"]))
        object.__setattr__(self, "wsgi_file_wrapper", environ.get("wsgi.file_wrapper", None))
        object.__setattr__(self, "wsgi_input_terminated", bool(environ.get("wsgi.input_terminated", False)))

        if self.wsgi_url_scheme not in ("http", "https"):
            raise UnsupportedProtocolError(
                f"Protocol '{self.wsgi_url_scheme}' does not supported. Only supported http or https protocols."
            )

        # CGI keys.
        object.__setattr__(self, "request_method", RequestMethod(environ["REQUEST_METHOD"]))
        object.__setattr__(self, "script_name", environ["SCRIPT_NAME"])
        object.__setattr__(self, "path_info", self._delete_redundant_slash(environ["PATH_INFO"]))
        object.__setattr__(self, "query_string", environ.get("QUERY_STRING", ""))
        object.__setattr__(self, "content_type", environ.get("CONTENT_TYPE", ""))
        object.__setattr__(self, "content_length", int(environ.get("CONTENT_LENGTH", 0) or 0))
        object.__setattr__(self, "server_name", environ["SERVER_NAME"])
        object.__setattr__(self, "server_port", int(environ["SERVER_PORT"]))
        object.__setattr__(self, "http_version", HttpVersion(environ["SERVER_PROTOCOL"]))

        # HTTP header.
        http_header = {}
        HTTP_KEY_PREFIX = "HTTP_"
        for key, value in environ.items():
            if key.startswith(HTTP_KEY_PREFIX):
                new_key = key.replace(HTTP_KEY_PREFIX, "")
                http_header[new_key] = value

        object.__setattr__(self, "http_header", http_header)

    def _delete_redundant_slash(self, path: str) -> str:
        return path if path[-1] != "/" else path[:-1]
