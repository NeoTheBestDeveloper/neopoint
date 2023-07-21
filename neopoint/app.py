import traceback
from typing import Any, Final, Iterable
from wsgiref.simple_server import make_server
from wsgiref.types import StartResponse

from neopoint.routing.route import Route

from .http import Request
from .wsgi import WsgiEnviron

__all__ = ("App",)


class App:
    """App class wich used as enter point for all library."""

    _root_route: Route
    _debug: Final[bool]

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug
        self._root_route = Route()

    def __call__(self, environ: dict[str, Any], start_response: StartResponse) -> Iterable[bytes]:
        status = "200 OK"
        headers = [(str("Content-type"), str("text/plain; charset=utf-8"))]

        try:
            wsgi_environ = WsgiEnviron(environ)
            request = Request(wsgi_environ)
            response = self._root_route.dispatch_request(request)
        # pylint: disable=broad-exception-caught
        except Exception:
            status = "500 Internal Server Error"
            headers = [(str("Content-type"), str("text/plain; charset=utf-8"))]
            response = str(traceback.format_exc()).encode("utf-8") if self._debug else b""

        start_response(status, headers)
        return [response]

    def run(self, host: str, port: int) -> None:
        with make_server(host, port, self) as httpd:
            httpd.serve_forever()

    def include_route(self, route: Route) -> None:
        self._root_route.include_route(route)
