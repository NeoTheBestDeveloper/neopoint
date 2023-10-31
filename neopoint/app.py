import traceback
from typing import Final, Iterable
from wsgiref.simple_server import make_server
from wsgiref.types import StartResponse, WSGIEnvironment

from neopoint.http.http_status import HttpStatus
from neopoint.http.path_params import PathParams
from neopoint.http.request import Request
from neopoint.http.response import Response, TextResponse

from .routing import Router
from .wsgi import WSGIEnvironmentDTO

__all__ = [
    "App",
]


class App:
    """App class which used as enter point for all library."""

    _root_route: Router
    _debug: Final[bool]

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug
        self._root_route = Router()

    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
        try:
            environ_dto = WSGIEnvironmentDTO(environ)
            response = self._handle_request(environ_dto)

        # pylint: disable=broad-exception-caught
        except Exception:
            response_text = str(traceback.format_exc()) if self._debug else ""
            response = TextResponse(response_text, status=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR)

        status = f"{response.status.status_code} {response.status.status_msg}"
        start_response(status, list(response.headers.items()))

        return [response.content]

    def _handle_request(self, environ_dto: WSGIEnvironmentDTO) -> Response:
        path_idx = self._root_route.find_path(environ_dto.path_info, environ_dto.request_method)

        if path_idx == -2:
            return TextResponse("Page not found.", status=HttpStatus.HTTP_404_NOT_FOUND)

        if path_idx == -1:
            return TextResponse("This method is not allowed.", status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED)

        path = self._root_route.pathes[path_idx]
        path_params = PathParams(environ_dto.path_info, path.pattern)
        request = Request(environ_dto, path_params)

        return path.controller(request)

    def run(self, host: str, port: int) -> None:
        with make_server(host, port, self) as httpd:
            httpd.serve_forever()

    def include_router(self, route: Router) -> None:
        self._root_route.include_router(route)
