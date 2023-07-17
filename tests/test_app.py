import pytest

from neopoint import App
from neopoint.utils.test_client import TestClient


@pytest.fixture
def app() -> App:
    return App()


@pytest.fixture
def client(app: App) -> TestClient:
    return TestClient(app)


def test_app_run(client: TestClient) -> None:
    with client as cl:
        req = cl.get("/")
        assert req.status_code == 200
        assert req.content == b"aboba"
