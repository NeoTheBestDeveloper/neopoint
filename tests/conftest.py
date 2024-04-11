import json
from io import BytesIO
from typing import Any
from wsgiref.util import setup_testing_defaults

import pytest


@pytest.fixture
def default_environ() -> dict[str, Any]:
    environ: dict[str, Any] = {}
    setup_testing_defaults(environ)
    return environ


@pytest.fixture
def json_for_post_json_environ() -> Any:
    return {
        "id": 123456,
        "title": "Cool title",
        "author_id": 342,
        "is_admin": False,
    }


@pytest.fixture
def post_json_environ(json_for_post_json_environ: Any) -> dict[str, Any]:
    environ: dict[str, Any] = {}
    setup_testing_defaults(environ)
    environ["REQUEST_METHOD"] = "POST"
    environ["CONTENT_TYPE"] = "application/json"

    content = json.dumps(json_for_post_json_environ).encode()

    environ["wsgi.input"] = BytesIO(content)
    environ["CONTENT_LENGTH"] = len(content)

    return environ
