import json
from io import BytesIO
from sys import stderr
from typing import Any, Callable, NoReturn
from wsgiref.types import WSGIApplication, WSGIEnvironment

from ..http import HttpMethod, HttpStatus, Response

__all__ = [
    "TestClient",
]


class TestClient:
    __test__ = False  # For pytest.

    _app: WSGIApplication
    _default_environ: WSGIEnvironment

    def __init__(self, app: WSGIApplication, server_name: str = "localhost", port: int = 80) -> None:
        self._app = app

        self._default_environ = {
            "REQUEST_METHOD": None,
            "SCRIPT_NAME": "",
            "PATH_INFO": "",
            "QUERY_STRING": "",
            "CONTENT_TYPE": "",
            "CONTENT_LENGTH": "",
            "SERVER_NAME": server_name,
            "SERVER_PORT": port,
            "SERVER_PROTOCOL": "HTTP/1.1",
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": BytesIO(),
            "wsgi.errors": stderr,
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
        }

    def _make_current_environ(self, path: str, method: HttpMethod, json_payload: bytes = b"") -> WSGIEnvironment:
        environ = self._default_environ.copy()

        if json_payload:
            environ["CONTENT_LENGTH"] = str(len(json_payload))
            environ["CONTENT_TYPE"] = "application/json"
        environ["wsgi.input"] = BytesIO(json_payload)

        if "?" in path:
            environ["PATH_INFO"], environ["QUERY_STRING"] = path.split("?")
        else:
            environ["PATH_INFO"] = path

        environ["REQUEST_METHOD"] = str(method)

        return environ

    def _handle_request(self, environ: WSGIEnvironment) -> Response | NoReturn:
        status_code: int | None = None
        response_headers = None
        exc_info = None

        def start_response(
            status_: str,
            response_headers_: list[tuple[str, str]],
            exc_info_: Any | None = None,
        ) -> Callable[[bytes], Any]:
            nonlocal status_code, response_headers, exc_info
            status_code = int(status_.split()[0])
            response_headers = response_headers_
            exc_info = exc_info_
            return lambda _: None

        content_by_parts = self._app(environ, start_response)
        content = b"".join(content_by_parts)

        assert status_code is not None
        assert response_headers is not None

        headers = dict(response_headers)
        media_type: str | None = None

        if headers.get("Content-Type", None) is not None:
            media_type = headers["Content-Type"].split(";")[0]

        return Response(
            status=HttpStatus(status_code),
            content=content,
            headers=headers,
            media_type=media_type,
        )

    def _json_to_bytes(self, json_payload: dict[str, Any]) -> bytes:
        return json.dumps(json_payload).encode()

    def get(self, path: str) -> Response:
        current_environ = self._make_current_environ(path, HttpMethod.GET)
        return self._handle_request(current_environ)

    def post(self, path: str, json_payload: dict[str, Any]) -> Response:
        bin_content = self._json_to_bytes(json_payload)
        current_environ = self._make_current_environ(path, HttpMethod.POST, bin_content)

        return self._handle_request(current_environ)

    def put(self, path: str, json_payload: dict[str, Any]) -> Response:
        bin_content = self._json_to_bytes(json_payload)
        current_environ = self._make_current_environ(path, HttpMethod.PUT, bin_content)

        return self._handle_request(current_environ)

    def delete(self, path: str) -> Response:
        current_environ = self._make_current_environ(path, HttpMethod.DELETE)
        return self._handle_request(current_environ)
