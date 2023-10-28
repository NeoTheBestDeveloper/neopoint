from typing import Callable, NoReturn, Self

from ..http import HttpStatus, Request, RequestMethod, Response, TextResponse
from .exceptions import ControllerRedefinitionError
from .url import Controller, Url

__all__ = [
    "Router",
]


class Router:
    _urls: list[Url]  # Urls stored with prefix
    _prefix: str

    def __init__(self, *, prefix: str = "") -> None:
        self._prefix = prefix
        self._urls = []

    def _find_url(self, path: str, method: RequestMethod) -> int:
        "Return positive index of found url or -1 if matched only by url, -2 if no match."

        matched_by_method = False
        for i, url in enumerate(self._urls):
            if url.match_by_path(path):
                if url.match_by_method(method):
                    return i
                matched_by_method = True

        return -1 if matched_by_method else -2

    def _append_url(self, url: Url) -> None | NoReturn:
        url_idx = self._find_url(url.path_pattern, url.method)

        if url_idx > -1:
            raise ControllerRedefinitionError(f"Controller '{url.controller.__name__}' already defined.")

        self._urls.append(url)
        return None

    def _append_endpoint(self, path: str, method: RequestMethod) -> Callable[[Controller], None]:
        if path not in ("/", ""):
            assert path.startswith("/"), "A path must start with '/'"
            assert not path.endswith("/"), "A path must not end with '/', as the routes will start with '/'"

        path = "" if path == "/" else path

        def decorator(controller: Controller) -> None:
            full_path = self._get_full_path(path)
            url_idx = self._find_url(full_path, method)

            if url_idx > -1:
                raise ControllerRedefinitionError(f"Controller {controller.__name__} already defined.")

            self._urls.append(Url(full_path, method, controller))

        return decorator

    def _get_full_path(self, path_part: str) -> str:
        return f"{self._prefix}{path_part}"

    def _delete_redundant_slash(self, path: str) -> str:
        return path if path[-1] != "/" else path[:-1]

    def get(self, path: str, *_) -> Callable[[Controller], None]:
        return self._append_endpoint(path, RequestMethod.GET)

    def post(self, path: str, *_) -> Callable[[Controller], None]:
        return self._append_endpoint(path, RequestMethod.POST)

    def put(self, path: str, *_) -> Callable[[Controller], None]:
        return self._append_endpoint(path, RequestMethod.PUT)

    def delete(self, path: str, *_) -> Callable[[Controller], None]:
        return self._append_endpoint(path, RequestMethod.DELETE)

    def include_router(self, other: Self) -> None:
        for url in other.urls:
            url.append_prefix(self._prefix)
            self._urls.append(url)

    def dispatch_request(self, request: Request) -> Response:
        path = self._delete_redundant_slash(request.path)

        idx = self._find_url(path, request.method)

        if idx == -2:
            return TextResponse("Page not found.", status=HttpStatus.HTTP_404_NOT_FOUND)

        if idx == -1:
            return TextResponse("This method is not allowed.", status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED)

        return self._urls[idx].controller(request)

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def urls(self) -> list[Url]:
        return self._urls.copy()
