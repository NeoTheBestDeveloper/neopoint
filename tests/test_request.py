from typing import Any

from neopoint.http.request import Request
from neopoint.wsgi.wsgi_environ import WSGIEnviron


def test_default_request(default_environ: dict[str, Any]):
    wsgi_environ = WSGIEnviron(default_environ)
    req = Request(wsgi_environ)
    assert req.content_length == wsgi_environ.content_length
    assert req.media_type == wsgi_environ.content_type
    assert req.path == wsgi_environ.path_info
    assert req.method == wsgi_environ.request_method
    assert req.headers == wsgi_environ.http_header.items().mapping
