import pytest

from neopoint.http.path_pattern import PathPattern


@pytest.mark.parametrize(
    "syntax_pattern,re_pattern",
    [
        ("/users/{id}", r"/users/(.+)"),
        ("/users/{user_id}/posts/{post_id}", r"/users/(.+)/posts/(.+)"),
        ("/users/{role}/{id}", r"/users/(.+)/(.+)"),
    ],
)
def test_path_pattern(syntax_pattern: str, re_pattern: str) -> None:
    pattern = PathPattern(syntax_pattern)
    assert pattern.syntax_pattern == syntax_pattern
    assert pattern.re_pattern.pattern == re_pattern


@pytest.mark.parametrize(
    "syntax_pattern,requested_pathes",
    [
        ("/users/{id}", ("/users/10", "/user/fasfsd")),
        ("/users/{user_id}/posts/{post_id}", ("/users/fdsafsdfas/posts/4", "/users/fsfds/fsfsd")),
        ("/users/{role}/{id}", ("/users/admin/23132", "/users//43242")),
    ],
)
def test_path_pattern_match(syntax_pattern: str, requested_pathes: tuple[str, ...]) -> None:
    pattern = PathPattern(syntax_pattern)
    assert pattern.match(requested_pathes[0]) is not None
    assert pattern.match(requested_pathes[1]) is None
