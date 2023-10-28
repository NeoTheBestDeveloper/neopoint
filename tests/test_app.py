import json
from typing import Any

import pytest

from neopoint import App
from neopoint.http import HttpStatus, JsonResponse, Request, Response, TextResponse
from neopoint.routing.router import Router
from neopoint.utils import TestClient


@pytest.fixture
def app() -> App:
    router = Router(prefix="/api")

    auth_router = Router(prefix="/auth")

    @auth_router.get("/user")
    def auth_user(*_: Request) -> Response:
        return TextResponse("Authorise user.")

    @router.get("/")
    def endpoint(*_: Any) -> Response:
        return TextResponse("Cool result.")

    @router.post("/theme")
    def create_theme(req: Request) -> Response:
        return JsonResponse(req.json)

    router.include_router(auth_router)

    app = App()
    app.include_router(router)

    return app


@pytest.fixture
def client(app: App) -> TestClient:
    return TestClient(app)


def test_app_run(client: TestClient) -> None:
    response = client.get("/api/?data=1&filter=category")
    assert response.status == HttpStatus(200)
    assert response.content == b"Cool result."
    assert response.media_type == "text/plain"


def test_get(client: TestClient) -> None:
    response = client.get("/api/auth/user")
    assert response.status == HttpStatus(200)
    assert response.content == b"Authorise user."
    assert response.media_type == "text/plain"


def test_post(client: TestClient) -> None:
    json_payload = {"id": 1, "title": "Cool theme title.", "authord_id": 1003}
    response = client.post("/api/theme", {"id": 1, "title": "Cool theme title.", "authord_id": 1003})
    assert response.status == HttpStatus(200)
    assert response.content == json.dumps(json_payload).encode()
    assert response.media_type == "application/json"


def test_not_found_error(client: TestClient) -> None:
    response = client.get("/some_fake_url")

    assert response.status == HttpStatus.HTTP_404_NOT_FOUND


def test_method_not_allowed_error(client: TestClient) -> None:
    response = client.delete("/api/auth/user")

    assert response.status == HttpStatus.HTTP_405_METHOD_NOT_ALLOWED
