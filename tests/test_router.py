from typing import Any

import pytest

from neopoint.http import Request, RequestMethod, Response, TextResponse
from neopoint.routing import Router
from neopoint.routing.exceptions import ControllerRedefinitionError
from neopoint.wsgi import WSGIEnvironmentDTO


@pytest.fixture
def get_request(default_environ: dict[str, Any]) -> Request:
    wsgi_environ = WSGIEnvironmentDTO(default_environ)
    return Request(wsgi_environ)


def test_adding_endpoint_get():
    router = Router()

    @router.get("/theme")
    def endpoint(*_: Request) -> Response:
        return TextResponse("aboba")

    # pylint: disable=protected-access
    assert router._find_url("/theme", RequestMethod.GET) != -1
    assert router._urls[0]._controller(None).content == b"aboba"


def test_controller_redefinition() -> None:
    router = Router()

    @router.get("/theme")
    def endpoint1(*_: Request) -> Response:
        return TextResponse("aboba")

    with pytest.raises(ControllerRedefinitionError):

        @router.get("/theme")
        def endpoint2(*_: Request) -> Response:
            return TextResponse("aboba")


def test_adding_endpoint_post():
    router = Router()

    @router.post("/theme")
    def endpoint(*_: Request) -> Response:
        return TextResponse("aboba")

    # pylint: disable=protected-access
    assert router._find_url("/theme", RequestMethod.POST) != -1
    assert router._urls[0]._controller(None).content == b"aboba"


def test_adding_endpoint_put():
    router = Router()

    @router.put("/theme")
    def endpoint(*_: Request) -> Response:
        return TextResponse("aboba")

    # pylint: disable=protected-access
    assert router._find_url("/theme", RequestMethod.PUT) != -1
    assert router._urls[0]._controller(None).content == b"aboba"


def test_adding_endpoint_delete():
    router = Router()

    @router.delete("/theme")
    def endpoint(*_: Request) -> Response:
        return TextResponse("aboba")

    # pylint: disable=protected-access
    assert router._find_url("/theme", RequestMethod.DELETE) != -1
    assert router._urls[0]._controller(None).content == b"aboba"


def test_router_include():
    root_router = Router(prefix="/api")

    theme_router = Router()

    @root_router.post("/auth")
    def auth(*_: Request) -> Response:
        return TextResponse("aboba auth")

    @theme_router.get("/theme")
    def get_theme(*_: Request) -> Response:
        return TextResponse("aboba get")

    @theme_router.delete("/theme")
    def delete_theme(*_: Request) -> Response:
        return TextResponse("aboba delete")

    root_router.include_router(theme_router)

    # pylint: disable=protected-access
    assert root_router._find_url("/api/auth", RequestMethod.POST) != -1
    assert root_router._urls[0]._controller(None).content == b"aboba auth"

    # pylint: disable=protected-access
    assert root_router._find_url("/api/theme", RequestMethod.GET) != -1
    assert root_router._urls[1]._controller(None).content == b"aboba get"

    # pylint: disable=protected-access
    assert root_router._find_url("/api/theme", RequestMethod.DELETE) != -1
    assert root_router._urls[2]._controller(None).content == b"aboba delete"


def test_route_dispatch_request(get_request: Request) -> None:
    router = Router()

    @router.get("/")
    def endpoint(*_: Request) -> Response:
        return TextResponse("aboba")

    res = router.dispatch_request(get_request)
    assert res.content == b"aboba"
