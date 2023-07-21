from typing import Any, Generator

import pytest

from neopoint import App
from neopoint.routing.route import Route
from neopoint.utils.test_client import TestClient


@pytest.fixture
def app() -> App:
    route = Route(prefix="/api")

    @route.get("/")
    def endpoint(*_: Any) -> bytes:
        return b"Cool result."

    app = App()
    app.include_route(route)

    return app


@pytest.fixture
def client(app: App) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


def test_app_run(client: TestClient) -> None:
    req = client.get("/api/")
    assert req.status_code == 200
    assert req.content == b"Cool result."
