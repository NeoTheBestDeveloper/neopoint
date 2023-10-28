import pytest

from neopoint.routing.url import Url


class FakeUrl(Url):
    # pylint: disable=super-init-not-called
    def __init__(self) -> None:
        ...


@pytest.mark.parametrize(
    "path_pattern,re_pattern",
    [
        ("/users/{id}", r"/users/(.+)"),
        ("/users/{user_id}/posts/{post_id}", r"/users/(.+)/posts/(.+)"),
        ("/users/{role}/{id}", r"/users/(.+)/(.+)"),
    ],
)
def test_path_pattern_to_re_parsing(path_pattern: str, re_pattern: str) -> None:
    # pylint: disable=protected-access
    assert FakeUrl()._get_re_pattern(path_pattern).pattern == re_pattern
