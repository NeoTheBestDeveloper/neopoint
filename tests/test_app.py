from multiprocessing import Process

import requests

from neopoint import App


def test_app_run() -> None:
    app = App()

    server_process = Process(target=app.run, args=["localhost", 8080])
    server_process.start()

    res = requests.get("http://localhost:8080")

    assert res.status_code == 200
    assert res.text == "aboba"

    server_process.kill()
