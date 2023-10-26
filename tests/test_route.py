from typing import Any

import pytest

from neopoint.http.http_status import HttpStatus
from neopoint.http.request import Request
from neopoint.http.request_method import RequestMethod
from neopoint.http.response import Response
from neopoint.routing import Route
from neopoint.wsgi.wsgi_environ import WSGIEnviron


@pytest.fixture
def get_request(default_environ: dict[str, Any]) -> Request:
    wsgi_environ = WSGIEnviron(default_environ)
    return Request(wsgi_environ)


def test_adding_endpoint_get():
    route = Route()

    @route.get("/theme")
    def endpoint(*_: Request) -> Response:
        return Response(HttpStatus.HTTP_200_OK, b"aboba", "text/plain; charset=utf-8")

    # pylint: disable=protected-access
    assert route._urls.get("/theme", None) is not None
    assert route._urls["/theme"][RequestMethod.GET](None).content == b"aboba"


def test_adding_endpoint_post():
    route = Route()

    @route.post("/theme")
    def endpoint(*_: Request) -> Response:
        return Response(HttpStatus.HTTP_200_OK, b"aboba", "text/plain; charset=utf-8")

    # pylint: disable=protected-access
    assert route._urls.get("/theme", None) is not None
    assert route._urls["/theme"][RequestMethod.POST](None).content == b"aboba"


def test_adding_endpoint_put():
    route = Route()

    @route.put("/theme")
    def endpoint(*_: Request) -> Response:
        return Response(HttpStatus.HTTP_200_OK, b"aboba", "text/plain; charset=utf-8")

    # pylint: disable=protected-access
    assert route._urls.get("/theme", None) is not None
    assert route._urls["/theme"][RequestMethod.PUT](None).content == b"aboba"


def test_adding_endpoint_delete():
    route = Route()

    @route.delete("/theme")
    def endpoint(*_: Request) -> Response:
        return Response(HttpStatus.HTTP_200_OK, b"aboba", "text/plain; charset=utf-8")

    # pylint: disable=protected-access
    assert route._urls.get("/theme", None) is not None
    assert route._urls["/theme"][RequestMethod.DELETE](None).content == b"aboba"


def test_route_include():
    root_route = Route(prefix="/api")

    theme_route = Route()

    @theme_route.get("/theme")
    def endpoint1(*_: Request) -> Response:
        return Response(HttpStatus.HTTP_200_OK, b"aboba get", "text/plain; charset=utf-8")

    @theme_route.delete("/theme")
    def endpoint2(*_: Request) -> Response:
        return Response(HttpStatus.HTTP_200_OK, b"aboba delete", "text/plain; charset=utf-8")

    root_route.include_route(theme_route)

    # pylint: disable=protected-access
    assert root_route._urls.get("/api/theme", None) is not None
    assert root_route._urls["/api/theme"][RequestMethod.DELETE](None).content == b"aboba delete"

    # pylint: disable=protected-access
    assert root_route._urls.get("/api/theme", None) is not None
    assert root_route._urls["/api/theme"][RequestMethod.GET](None).content == b"aboba get"


def test_route_dispatch_request(get_request: Request) -> None:
    route = Route()

    @route.get("/")
    def endpoint(*_: Request) -> Response:
        return Response(HttpStatus.HTTP_200_OK, b"aboba", "text/plain; charset=utf-8")

    res = route.dispatch_request(get_request)
    assert res.content == b"aboba"
