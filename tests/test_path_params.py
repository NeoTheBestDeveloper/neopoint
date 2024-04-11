import pytest

from neopoint.http.path_params import PathParams
from neopoint.http.request_method import RequestMethod
from neopoint.http.response import TextResponse
from neopoint.routing.path import Path


class FakePath(Path):
    def __init__(self, path: str) -> None:
        super().__init__(path, RequestMethod.GET, lambda *_: TextResponse(""))


@pytest.mark.parametrize(
    "path,requested_path,dict_res",
    [
        (FakePath("/users/{id}"), "/users/231", {"id": "231"}),
        (
            FakePath("/users/{user_id}/posts/{post_id}"),
            "/users/321/posts/432432",
            {"user_id": "321", "post_id": "432432"},
        ),
        (FakePath("/users/{role}/{id}"), "/users/admin/80954", {"role": "admin", "id": "80954"}),
    ],
)
def test_path_params_parsing(path: FakePath, requested_path: str, dict_res: dict[str, str]) -> None:
    assert dict(PathParams(requested_path, path.pattern)) == dict_res
