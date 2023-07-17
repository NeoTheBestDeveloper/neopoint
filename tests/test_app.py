from multiprocessing import Process

import requests
from requests import exceptions
from urllib3.exceptions import MaxRetryError

from neopoint import App


def test_app_run() -> None:
    app = App()

    server_process = Process(target=app.run, args=["localhost", 8080])
    server_process.start()

    try:
        res = requests.get("http://localhost:8080", timeout=20)

        assert res.status_code == 200
        assert res.text == "aboba"
    except MaxRetryError as e:
        print(e)
        server_process.kill()
        assert False
    except exceptions.ConnectionError as e:
        print(e)
        server_process.kill()
        assert False
    server_process.kill()
