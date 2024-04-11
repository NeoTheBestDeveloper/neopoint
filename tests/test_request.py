from typing import Any

from neopoint.http import Request
from neopoint.http.path_params import PathParams
from neopoint.http.path_pattern import PathPattern
from neopoint.wsgi import WSGIEnvironmentDTO


class FakeRequest(Request):
    def __init__(self, wsgi_environ: WSGIEnvironmentDTO) -> None:
        super().__init__(wsgi_environ, PathParams("", PathPattern("")))


def test_get_request(default_environ: dict[str, Any]):
    wsgi_environ = WSGIEnvironmentDTO(default_environ)
    req = FakeRequest(wsgi_environ)

    assert len(req.content) == wsgi_environ.content_length
    assert req.media_type == wsgi_environ.content_type
    assert req.path == wsgi_environ.path_info
    assert req.method == wsgi_environ.request_method
    assert req.headers == wsgi_environ.http_header.items().mapping
    assert not req.query_params


def test_post_request(post_json_environ: dict[str, Any]):
    wsgi_environ = WSGIEnvironmentDTO(post_json_environ)
    req = FakeRequest(wsgi_environ)
    req_headers = dict(req.headers)
    del req_headers["Content-Type"]
    del req_headers["Content-Length"]

    assert len(req.content) == wsgi_environ.content_length
    assert req.media_type == wsgi_environ.content_type
    assert req.path == wsgi_environ.path_info
    assert req.method == wsgi_environ.request_method
    assert req_headers == wsgi_environ.http_header.items().mapping
