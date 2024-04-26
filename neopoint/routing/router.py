from typing import Callable, NoReturn, Self

from neopoint.http.request_method import RequestMethod

from .exceptions import ControllerRedefinitionError
from .path import Controller, Path

__all__ = [
    "Router",
]


class Router:
    _pathes: list[Path]  # Pathes stored with prefix
    _prefix: str

    def __init__(self, *, prefix: str = "") -> None:
        self._prefix = prefix
        self._pathes = []

    def find_path(self, searched_path: str, method: RequestMethod) -> int:
        "Return positive index of found url or -1 if matched only by url, -2 if no match."

        matched_by_method = False
        for i, path in enumerate(self._pathes):
            if path.match_by_path(searched_path):
                if path.match_by_method(method):
                    return i
                matched_by_method = True

        return -1 if matched_by_method else -2

    def _append_path(self, path: Path) -> None | NoReturn:
        path_idx = self.find_path(path.pattern.syntax_pattern, path.method)

        if path_idx > -1:
            raise ControllerRedefinitionError(f"Controller '{path.controller.__name__}' already defined.")

        self._pathes.append(path)
        return None

    def _append_endpoint(self, path: str, method: RequestMethod) -> Callable[[Controller], None]:
        if path not in ("/", ""):
            assert path.startswith("/"), "A path must start with '/'"
            assert not path.endswith("/"), "A path must not end with '/', as the routes will start with '/'"

        path = "" if path == "/" else path

        def controller_wrapper(controller: Controller) -> None:
            full_path = self._get_full_path(path)
            path_idx = self.find_path(full_path, method)

            if path_idx > -1:
                raise ControllerRedefinitionError(f"Controller {controller.__name__} already defined.")

            new_path = Path(full_path, method, controller)
            self._append_path(new_path)

        return controller_wrapper

    def _get_full_path(self, path_part: str) -> str:
        return f"{self._prefix}{path_part}"

    def get(self, path: str, *_) -> Callable[[Controller], None]:
        return self._append_endpoint(path, RequestMethod.GET)

    def post(self, path: str, *_) -> Callable[[Controller], None]:
        return self._append_endpoint(path, RequestMethod.POST)

    def put(self, path: str, *_) -> Callable[[Controller], None]:
        return self._append_endpoint(path, RequestMethod.PUT)

    def delete(self, path: str, *_) -> Callable[[Controller], None]:
        return self._append_endpoint(path, RequestMethod.DELETE)

    def include_router(self, other: Self) -> None:
        for path in other.pathes:
            path.append_prefix(self._prefix)
            self._append_path(path)

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def pathes(self) -> list[Path]:
        return self._pathes.copy()
