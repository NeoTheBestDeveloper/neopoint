from multiprocessing import Process
from typing import Self

import requests

from ..app import App


class TestClient:
    __test__ = False  # For pytest.

    _app: App
    _app_process: Process
    _url: str
    _port: int

    def __init__(self, wsgi_app: App, url: str = "localhost", port: int = 8080) -> None:
        self._app = wsgi_app
        self._url = url
        self._port = port
        self._app_process = Process(target=self._app.run, args=[url, port])
        self._app_process.start()

        server_started = False

        while not server_started:
            try:
                requests.get(f"http://{url}:{port}", timeout=1)
                server_started = True
            except requests.exceptions.ConnectionError:
                ...

    def _get_full_url(self, url_part: str) -> str:
        return f"http://{self._url}:{self._port}{url_part}"

    def get(self, url_part: str, timeout: float = 2.0) -> requests.Response:
        return requests.get(self._get_full_url(url_part), timeout=timeout)

    def post(self, url_part: str, json: dict | None = None, timeout: float = 2.0) -> requests.Response:
        return requests.post(self._get_full_url(url_part), json=json, timeout=timeout)

    def kill(self) -> None:
        self._app_process.kill()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        self.kill()
