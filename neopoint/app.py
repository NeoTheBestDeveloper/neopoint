from typing import Final, Iterable
from wsgiref.simple_server import make_server
from wsgiref.types import StartResponse, WSGIEnvironment

from .http import HttpStatus, Request, Response
from .routing import Route
from .wsgi import WSGIEnviron

__all__ = ("App",)


class App:
    """App class which used as enter point for all library."""

    _root_route: Route
    _debug: Final[bool]

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug
        self._root_route = Route()

    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
        try:
            wsgi_environ = WSGIEnviron(environ)
            request = Request(wsgi_environ)
            response = self._root_route.dispatch_request(request)

        # pylint: disable=broad-exception-caught
        except Exception:
            response = Response(HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR)

        status = f"{response.status.status_code} {response.status.status_msg}"
        start_response(status, [response.headers.items()])

        return [response.content]

    def run(self, host: str, port: int) -> None:
        with make_server(host, port, self) as httpd:
            httpd.serve_forever()

    def include_route(self, route: Route) -> None:
        self._root_route.include_route(route)
