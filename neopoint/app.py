import traceback
from typing import Final, Iterable
from wsgiref.simple_server import make_server
from wsgiref.types import StartResponse, WSGIEnvironment

from neopoint.http.response import TextResponse

from .http import HttpStatus, Request
from .routing import Route
from .wsgi import WSGIEnvironmentDTO

__all__ = [
    "App",
]


class App:
    """App class which used as enter point for all library."""

    _root_route: Route
    _debug: Final[bool]

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug
        self._root_route = Route()

    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
        print(environ)
        try:
            environ_dto = WSGIEnvironmentDTO(environ)
            request = Request(environ_dto)
            response = self._root_route.dispatch_request(request)

        # pylint: disable=broad-exception-caught
        except Exception:
            response_text = str(traceback.format_exc()) if self._debug else ""
            response = TextResponse(response_text, status=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR)

        status = f"{response.status.status_code} {response.status.status_msg}"
        start_response(status, list(response.headers.items()))

        return [response.content]

    def run(self, host: str, port: int) -> None:
        with make_server(host, port, self) as httpd:
            httpd.serve_forever()

    def include_route(self, route: Route) -> None:
        self._root_route.include_route(route)
