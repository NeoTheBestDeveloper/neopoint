import pytest

from neopoint.http.request_method import RequestMethod
from neopoint.http.response import TextResponse
from neopoint.routing.path_params import PathParams
from neopoint.routing.url import Url


class FakeUrl(Url):
    def __init__(self, path: str) -> None:
        super().__init__(path, RequestMethod.GET, lambda *_: TextResponse(""))


@pytest.mark.parametrize(
    "url,requested_path,dict_res",
    [
        (FakeUrl("/users/{id}"), "/users/231", {"id": "231"}),
        (
            FakeUrl("/users/{user_id}/posts/{post_id}"),
            "/users/321/posts/432432",
            {"user_id": "321", "post_id": "432432"},
        ),
        (FakeUrl("/users/{role}/{id}"), "/users/admin/80954", {"role": "admin", "id": "80954"}),
    ],
)
def test_path_params_parsing(url: FakeUrl, requested_path: str, dict_res: dict[str, str]) -> None:
    assert dict(PathParams(requested_path, url)) == dict_res
