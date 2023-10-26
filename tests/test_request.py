from typing import Any

from neopoint.http import Request
from neopoint.wsgi import WSGIEnvironmentDTO


def test_get_request(default_environ: dict[str, Any]):
    wsgi_environ = WSGIEnvironmentDTO(default_environ)
    req = Request(wsgi_environ)

    assert len(req.content) == wsgi_environ.content_length
    assert req.media_type == wsgi_environ.content_type
    assert req.path == wsgi_environ.path_info
    assert req.method == wsgi_environ.request_method
    assert req.headers == wsgi_environ.http_header.items().mapping


def test_post_request(post_json_environ: dict[str, Any]):
    wsgi_environ = WSGIEnvironmentDTO(post_json_environ)
    req = Request(wsgi_environ)
    req_headers = dict(req.headers)
    del req_headers["Content-Type"]
    del req_headers["Content-Length"]

    assert len(req.content) == wsgi_environ.content_length
    assert req.media_type == wsgi_environ.content_type
    assert req.path == wsgi_environ.path_info
    assert req.method == wsgi_environ.request_method
    assert req_headers == wsgi_environ.http_header.items().mapping
