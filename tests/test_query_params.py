import pytest

from neopoint.http.query_params import QueryParams


@pytest.mark.parametrize(
    "query_string,dict_res",
    [
        ("name=john&age=15", {"name": "john", "age": "15"}),
        ("password=aboba", {"password": "aboba"}),
        ("", {}),
    ],
)
def test_query_params_parsing(query_string: str, dict_res: dict[str, str]) -> None:
    assert dict(QueryParams(query_string)) == dict_res


@pytest.mark.parametrize(
    "query_string,dict_res",
    [
        ("names=john&names=diana&age=15", {"names": ["john", "diana"], "age": "15"}),
        ("age=15&names=john,diana", {"names": ["john", "diana"], "age": "15"}),
        ("age=15&names=john,diana&names=jack,bob", {"names": ["john", "diana", "jack", "bob"], "age": "15"}),
        ("age=15&names=john,diana&names=jack", {"names": ["john", "diana", "jack"], "age": "15"}),
    ],
)
def test_query_params_arrays_parsing(query_string: str, dict_res: dict[str, str]) -> None:
    assert dict(QueryParams(query_string)) == dict_res


@pytest.mark.parametrize(
    "query_string,dict_res",
    [
        ("age=15&name=john%20john%20aboba", {"name": "john john aboba", "age": "15"}),
    ],
)
def test_query_params_parsing_with_decoding(query_string: str, dict_res: dict[str, str]) -> None:
    assert dict(QueryParams(query_string)) == dict_res
