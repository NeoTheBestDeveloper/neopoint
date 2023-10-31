from typing import Any

import pytest

from neopoint.http import Request, RequestMethod, Response, TextResponse
from neopoint.http.path_params import PathParams
from neopoint.http.path_pattern import PathPattern
from neopoint.routing import Router
from neopoint.routing.exceptions import ControllerRedefinitionError
from neopoint.wsgi import WSGIEnvironmentDTO


class FakeRequest(Request):
    def __init__(self, wsgi_environ: WSGIEnvironmentDTO) -> None:
        super().__init__(wsgi_environ, PathParams("", PathPattern("")))


@pytest.fixture
def get_request(default_environ: dict[str, Any]) -> Request:
    wsgi_environ = WSGIEnvironmentDTO(default_environ)
    return FakeRequest(wsgi_environ)


def test_adding_endpoint_get():
    router = Router()

    @router.get("/theme")
    def endpoint(*_: Request) -> Response:
        return TextResponse("aboba")

    assert router.find_path("/theme", RequestMethod.GET) != -1
    assert router.pathes[0].controller(None).content == b"aboba"


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

    assert router.find_path("/theme", RequestMethod.POST) != -1
    assert router.pathes[0].controller(None).content == b"aboba"


def test_adding_endpoint_put():
    router = Router()

    @router.put("/theme")
    def endpoint(*_: Request) -> Response:
        return TextResponse("aboba")

    assert router.find_path("/theme", RequestMethod.PUT) != -1
    assert router.pathes[0].controller(None).content == b"aboba"


def test_adding_endpoint_delete():
    router = Router()

    @router.delete("/theme")
    def endpoint(*_: Request) -> Response:
        return TextResponse("aboba")

    assert router.find_path("/theme", RequestMethod.DELETE) != -1
    assert router.pathes[0].controller(None).content == b"aboba"


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

    assert root_router.find_path("/api/auth", RequestMethod.POST) > -1
    assert root_router.pathes[0].controller(None).content == b"aboba auth"

    assert root_router.find_path("/api/theme", RequestMethod.GET) > -1
    assert root_router.pathes[1].controller(None).content == b"aboba get"

    assert root_router.find_path("/api/theme", RequestMethod.DELETE) > -1
    assert root_router.pathes[2].controller(None).content == b"aboba delete"
