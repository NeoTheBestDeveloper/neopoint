from typing import Any, Generator

import pytest

from neopoint import App
from neopoint.http.http_status import HttpStatus
from neopoint.http.request import Request
from neopoint.http.response import Response
from neopoint.routing.route import Route
from neopoint.utils.test_client import TestClient


@pytest.fixture
def app() -> App:
    route = Route(prefix="/api")

    @route.get("/")
    def endpoint(*_: Any) -> Response:
        return Response(HttpStatus.HTTP_200_OK, b"Cool result.", "text/plain; charset=utf-8")

    @route.post("/theme")
    def create_theme(req: Request) -> Response:
        json = req.json
        return Response(HttpStatus.HTTP_200_OK, json["title"].encode(), "text/plain; charset=utf-8")

    app = App()
    app.include_route(route)

    return app


@pytest.fixture
def client(app: App) -> Generator[TestClient, None, None]:
    yield TestClient(app)


def test_app_run(client: TestClient) -> None:
    response = client.get("/api/?data=1&filter=category")
    assert response.status_code == 200
    assert response.content == b"Cool result."


def test_post(client: TestClient) -> None:
    response = client.post("/api/theme", {"id": 1, "title": "Cool theme title.", "authord_id": 1003})
    assert response.status_code == 200
    assert response.content == b"Cool theme title."
