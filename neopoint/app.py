from typing import Any, Final, Iterable
from wsgiref.simple_server import make_server
from wsgiref.types import StartResponse

from .http import Request
from .wsgi import UnsupportedProtocol, WsgiEnviron

__all__ = ("App",)


class App:
    """App class wich used as enter point for all library."""

    _debug: Final[bool]

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug

    def __call__(self, environ: dict[str, Any], start_response: StartResponse) -> Iterable[bytes]:
        status = "200 OK"
        headers = [(str("Content-type"), str("text/plain; charset=utf-8"))]

        try:
            wsgi_environ = WsgiEnviron(environ)
        except UnsupportedProtocol:
            return [f"Protocol {environ['wsgi.url_schema']} does not supported.".encode("utf-8")]
        except AttributeError as e:
            return [f"{e}".encode("utf-8")]

        Request(wsgi_environ)

        start_response(status, headers)
        return ["aboba".encode("utf-8")]

    def run(self, host: str, port: int) -> None:
        with make_server(host, port, self) as httpd:
            httpd.serve_forever()
