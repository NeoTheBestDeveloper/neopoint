import json
from dataclasses import astuple
from typing import Any
from wsgiref.types import WSGIEnvironment

import pytest

from neopoint.http import RequestMethod
from neopoint.wsgi import WSGIEnvironmentDTO, WSGIVersion
from neopoint.wsgi.exceptions import UnsupportedProtocolError


def test_default_wsgi_environ(default_environ: WSGIEnvironment) -> None:
    wsgi_environ = WSGIEnvironmentDTO(default_environ)
    assert wsgi_environ.wsgi_version == WSGIVersion(1, 0)
    assert wsgi_environ.wsgi_url_scheme == "http"
    assert wsgi_environ.wsgi_input.read() == b""
    assert wsgi_environ.wsgi_errors.read() == ""
    assert not wsgi_environ.wsgi_multiprocess
    assert not wsgi_environ.wsgi_multithread
    assert not wsgi_environ.wsgi_run_once

    assert wsgi_environ.request_method == RequestMethod.GET
    assert wsgi_environ.script_name == ""
    assert wsgi_environ.path_info == "/"
    assert wsgi_environ.query_string == ""
    assert wsgi_environ.content_type == ""
    assert wsgi_environ.content_length == 0
    assert wsgi_environ.server_name == "127.0.0.1"
    assert wsgi_environ.server_port == 80
    assert astuple(wsgi_environ.http_version) == (1, 0)
    assert wsgi_environ.http_header == {"HOST": "127.0.0.1"}


def test_post_json_wsgi_environ(post_json_environ: WSGIEnvironment, json_for_post_json_environ: dict[str, Any]) -> None:
    content = json.dumps(json_for_post_json_environ).encode()
    wsgi_environ = WSGIEnvironmentDTO(post_json_environ)

    assert wsgi_environ.wsgi_version == WSGIVersion(1, 0)
    assert wsgi_environ.wsgi_url_scheme == "http"
    assert wsgi_environ.wsgi_input.read() == content
    assert wsgi_environ.wsgi_errors.read() == ""
    assert not wsgi_environ.wsgi_multiprocess
    assert not wsgi_environ.wsgi_multithread
    assert not wsgi_environ.wsgi_run_once

    assert wsgi_environ.request_method == RequestMethod.POST
    assert wsgi_environ.script_name == ""
    assert wsgi_environ.path_info == "/"
    assert wsgi_environ.query_string == ""
    assert wsgi_environ.content_type == "application/json"
    assert wsgi_environ.content_length == len(content)
    assert wsgi_environ.server_name == "127.0.0.1"
    assert wsgi_environ.server_port == 80
    assert astuple(wsgi_environ.http_version) == (1, 0)
    assert wsgi_environ.http_header == {"HOST": "127.0.0.1"}


def test_invalid_protocol_for_wsgi_environ(default_environ: dict[str, Any]) -> None:
    default_environ["wsgi.url_scheme"] = "ftp"

    with pytest.raises(UnsupportedProtocolError):
        WSGIEnvironmentDTO(default_environ)
