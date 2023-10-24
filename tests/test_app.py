from typing import Any, Generator

import pytest

from neopoint import App
from neopoint.http.request import Request
from neopoint.routing.route import Route
from neopoint.utils.test_client import TestClient


@pytest.fixture
def app() -> App:
    route = Route(prefix="/api")

    @route.get("/")
    def endpoint(*_: Any) -> bytes:
        return b"Cool result."

    @route.post("/theme")
    def create_theme(req: Request) -> bytes:
        json = req.json
        return json["title"].encode()

    app = App()
    app.include_route(route)

    return app


@pytest.fixture
def client(app: App) -> Generator[TestClient, None, None]:
    yield TestClient(app)


def test_app_run(client: TestClient) -> None:
    req = client.get("/api/?data=1&filter=category")
    assert req.status_code == 200
    assert req.content == b"Cool result."


def test_post(client: TestClient) -> None:
    req = client.post("/api/theme", {"id": 1, "title": "Cool theme title.", "authord_id": 1003})
    assert req.status_code == 200
    assert req.content == b"Cool theme title."
