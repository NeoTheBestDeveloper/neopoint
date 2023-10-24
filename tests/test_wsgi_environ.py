from dataclasses import astuple
from typing import Any
from wsgiref.util import setup_testing_defaults

import pytest

from neopoint.http.request_method import RequestMethod
from neopoint.wsgi import WSGIEnviron
from neopoint.wsgi.exceptions import UnsupportedProtocol
from neopoint.wsgi.wsgi_version import WsgiVersion


@pytest.fixture
def default_environ() -> dict[str, Any]:
    environ: dict[str, Any] = {}
    setup_testing_defaults(environ)
    return environ


def test_default_wsgi_environ(default_environ: dict[str, Any]) -> None:
    wsgi_environ = WSGIEnviron(default_environ)
    assert wsgi_environ.wsgi_version == WsgiVersion(1, 0)
    assert wsgi_environ.wsgi_url_scheme == "http"
    assert wsgi_environ.wsgi_input.read() == b""
    assert wsgi_environ.wsgi_errors.read() == ""
    assert not wsgi_environ.wsgi_multiprocess
    assert not wsgi_environ.wsgi_multithread
    assert not wsgi_environ.wsgi_run_once

    assert wsgi_environ.request_method == RequestMethod("GET")
    assert wsgi_environ.script_name == ""
    assert wsgi_environ.path_info == "/"
    assert wsgi_environ.query_string == ""
    assert wsgi_environ.content_type == ""
    assert wsgi_environ.content_length == 0
    assert wsgi_environ.server_name == "127.0.0.1"
    assert wsgi_environ.server_port == 80
    assert astuple(wsgi_environ.http_version) == (1, 0)
    assert wsgi_environ.http_header == {"HOST": "127.0.0.1"}


def test_invalid_protocal_for_wsgi_environ(default_environ: dict[str, Any]) -> None:
    default_environ["wsgi.url_scheme"] = "ftp"

    with pytest.raises(UnsupportedProtocol):
        WSGIEnviron(default_environ)
