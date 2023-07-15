from typing import Any
from wsgiref.util import setup_testing_defaults

import pytest

from neopoint.http.request import Request
from neopoint.wsgi.wsgi_environ import WsgiEnviron


@pytest.fixture
def default_environ() -> dict[str, Any]:
    environ: dict[str, Any] = {}
    setup_testing_defaults(environ)
    return environ


def test_default_request(default_environ: dict[str, Any]):
    wsgi_environ = WsgiEnviron(default_environ)
    req = Request(wsgi_environ)
    assert req.content_length == wsgi_environ.content_length
    assert req.content_type == wsgi_environ.content_type
    assert req.path == wsgi_environ.path_info
    assert req.method == wsgi_environ.request_method
    assert req.header == wsgi_environ.http_header.items().mapping
