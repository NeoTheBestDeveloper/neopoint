from typing import Any
from wsgiref.util import setup_testing_defaults

import pytest


@pytest.fixture
def default_environ() -> dict[str, Any]:
    environ: dict[str, Any] = {}
    setup_testing_defaults(environ)
    return environ


def test_default_request(default_environ: dict[str, Any]):
    assert True
