import pytest

from neopoint.http.request_method import RequestMethod
from neopoint.http.response import TextResponse
from neopoint.routing.path import Path


class FakePath(Path):
    def __init__(self, path: str) -> None:
        super().__init__(path, RequestMethod.GET, lambda *_: TextResponse(""))


@pytest.mark.parametrize(
    "syntax_pattern,requested_path",
    [
        (
            "/users/{id}",
            "/users/fsdfksj",
        ),
        (
            "/users/{user_id}/posts/{post_id}",
            "/users/423423/posts/fsf",
        ),
        (
            "/users/{role}/{id}",
            "/users/fadsfas/43242",
        ),
    ],
)
def test_path_match_by_path(syntax_pattern: str, requested_path: str) -> None:
    path = FakePath(syntax_pattern)
    assert path.match_by_path(requested_path)


@pytest.mark.parametrize(
    "syntax_pattern,requested_path",
    [
        (
            "/users/{id}",
            "/users/fsdfksj/fs",
        ),
        (
            "/users/{user_id}/posts/{post_id}",
            "/users//posts/fsf",
        ),
        (
            "/users/{role}/{id}",
            "/users/fadsfas",
        ),
    ],
)
def test_path_dont_math_by_path(syntax_pattern: str, requested_path: str) -> None:
    path = FakePath(syntax_pattern)
    assert not path.match_by_path(requested_path)
