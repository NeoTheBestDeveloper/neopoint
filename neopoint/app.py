import traceback
from typing import Any, Final, Iterable, NoReturn
from wsgiref.simple_server import make_server
from wsgiref.types import StartResponse, WSGIEnvironment

from neopoint.http.http_status import HttpStatus
from neopoint.http.path_params import PathParams
from neopoint.http.query_params import QueryParams
from neopoint.http.request import Request
from neopoint.http.response import Response, TextResponse
from neopoint.routing.path import Controller

from .exceptions import ControllerArgumentsParsingError
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
        print(environ)
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

        return self._call_controller(request, path.controller)

    def _has_request_annotation(self, args_annotations: dict[str, Any]) -> bool:
        return Request in args_annotations.values()

    def _get_return_annotation(self, annotations: dict[str, Any]) -> str:
        if "return" in annotations:
            return annotations["return"]
        return ""

    def _get_args_annotations(self, annotations: dict[str, Any]) -> dict[str, Any]:
        annotations_copy = annotations.copy()
        if "return" in annotations_copy:
            del annotations_copy["return"]
        return annotations_copy

    def _parse_path_params(self, args_annotations: dict[str, Any], path_params: PathParams) -> dict[str, Any]:
        res: dict[str, Any] = {}

        for name, type_ in args_annotations.items():
            if name in path_params:
                res[name] = type_(path_params[name])

        return res

    def _parse_query_params(self, args_annotations: dict[str, Any], query_params: QueryParams) -> dict[str, Any]:
        res: dict[str, Any] = {}

        for name, type_ in args_annotations.items():
            if name in query_params:
                res[name] = type_(query_params[name])

        return res

    def _call_controller(self, request: Request, controller: Controller) -> Response | NoReturn:
        annotations = controller.__annotations__
        # return_annotation = self._get_return_annotation(annotations)
        args_annotations = self._get_args_annotations(annotations)

        if self._has_request_annotation(args_annotations):
            if len(args_annotations) == 1:
                return controller(request)
            raise ControllerArgumentsParsingError(
                "Only one argument must be for controller if you using 'low-level syntax' (Request annotation). "
                f"Controller name={controller.__name__}"
            )

        path_params = self._parse_path_params(args_annotations, request.path_params)
        query_params = self._parse_query_params(args_annotations, request.query_params)

        return controller(**path_params, **query_params)

    def run(self, host: str, port: int) -> None:
        with make_server(host, port, self) as httpd:
            httpd.serve_forever()

    def include_router(self, route: Router) -> None:
        self._root_route.include_router(route)
