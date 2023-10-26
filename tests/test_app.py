import json
from typing import Any

import pytest

from neopoint import App
from neopoint.http.http_status import HttpStatus
from neopoint.http.request import Request
from neopoint.http.response import JsonResponse, Response, TextResponse
from neopoint.routing.route import Route
from neopoint.utils.test_client import TestClient


@pytest.fixture
def app() -> App:
    route = Route(prefix="/api")

    @route.get("/")
    def endpoint(*_: Any) -> Response:
        return TextResponse("Cool result.")

    @route.post("/theme")
    def create_theme(req: Request) -> Response:
        return JsonResponse(req.json)

    app = App()
    app.include_route(route)

    return app


@pytest.fixture
def client(app: App) -> TestClient:
    return TestClient(app)


def test_app_run(client: TestClient) -> None:
    response = client.get("/api/?data=1&filter=category")
    assert response.status == HttpStatus(200)
    assert response.content == b"Cool result."
    assert response.media_type == "text/plain"


def test_post(client: TestClient) -> None:
    json_payload = {"id": 1, "title": "Cool theme title.", "authord_id": 1003}
    response = client.post("/api/theme", {"id": 1, "title": "Cool theme title.", "authord_id": 1003})
    assert response.status == HttpStatus(200)
    assert response.content == json.dumps(json_payload).encode()
    assert response.media_type == "application/json"
