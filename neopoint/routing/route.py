from typing import Any, Callable, Iterator, Self, TypeAlias

from ..http import Request, RequestMethod

EndpointCallable: TypeAlias = Callable[[Any], bytes]

__all__ = ("Route",)


class Route:
    _prefix: str
    _urls: dict[str, dict[RequestMethod, EndpointCallable]]

    def __init__(self, *, prefix: str = "") -> None:
        if prefix:
            assert prefix.startswith("/"), "A path prefix must start with '/'"
            assert not prefix.endswith("/"), "A path prefix must not end with '/', as the routes will start with '/'"

        self._prefix = prefix
        self._urls = {}

    def _append_endpoint(self, path: str, method: RequestMethod) -> Callable[[EndpointCallable], None]:
        if path not in ("/", ""):
            assert path.startswith("/"), "A path must start with '/'"
            assert not path.endswith("/"), "A path must not end with '/', as the routes will start with '/'"

        def decorator(endpoint: EndpointCallable) -> None:
            if self._urls.get(path) is None:
                self._urls[self._prefix + path] = {method: endpoint}
            else:
                self._urls[self._prefix + path][method] = endpoint

        return decorator

    def __iter__(self) -> Iterator[tuple[str, dict[RequestMethod, EndpointCallable]]]:
        return iter(self._urls.items())

    def get(self, path: str, *_) -> Callable[[EndpointCallable], None]:
        return self._append_endpoint(path, RequestMethod.GET)

    def post(self, path: str, *_) -> Callable[[EndpointCallable], None]:
        return self._append_endpoint(path, RequestMethod.POST)

    def put(self, path: str, *_) -> Callable[[EndpointCallable], None]:
        return self._append_endpoint(path, RequestMethod.PUT)

    def delete(self, path: str, *_) -> Callable[[EndpointCallable], None]:
        return self._append_endpoint(path, RequestMethod.DELETE)

    def include_route(self, route: Self) -> None:
        for url_part, endpoints in route:
            url = f"{self._prefix}{url_part}"
            self._urls[url] = endpoints

    def dispatch_request(self, req: Request) -> bytes:
        if self._urls.get(req.path) is None:
            return b"Not found 404 Error."
        if self._urls[req.path].get(req.method) is None:
            return b"This method is allowed."

        return self._urls[req.path][req.method](req)
