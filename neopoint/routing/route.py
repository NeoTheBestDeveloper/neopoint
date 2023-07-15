__all__ = ("Route",)


from typing import Any, Callable, TypeAlias

from ..http import RequestMethod

EndpointType: TypeAlias = Callable[[Any], bytes]


class Route:
    _urls: dict[str, tuple[RequestMethod, Callable]]

    def __init__(self) -> None:
        self._urls = {}

    def _append_endpoint(self, path: str, method: RequestMethod) -> Callable[[EndpointType], None]:
        def decorator(endpoint: EndpointType) -> None:
            self._urls[path] = (method, endpoint)

        return decorator

    def get(self, path: str, *_) -> Callable[[EndpointType], None]:
        return self._append_endpoint(path, RequestMethod.GET)

    def post(self, path: str, *_) -> Callable[[EndpointType], None]:
        return self._append_endpoint(path, RequestMethod.POST)

    def put(self, path: str, *_) -> Callable[[EndpointType], None]:
        return self._append_endpoint(path, RequestMethod.PUT)

    def delete(self, path: str, *_) -> Callable[[EndpointType], None]:
        return self._append_endpoint(path, RequestMethod.DELETE)
