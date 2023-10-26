from dataclasses import astuple

import pytest

from neopoint.http import HttpVersion
from neopoint.http.exceptions import InvalidHttpVersionError


@pytest.mark.parametrize(
    "version,expected_version",
    [
        ("HTTP/1.0", (1, 0)),
        ("HTTP/1.1", (1, 1)),
        ("HTTP/2", (2, 0)),
        ("HTTP/3", (3, 0)),
    ],
)
def test_http_version_parsing(version: str, expected_version: tuple[int, int]) -> None:
    assert astuple(HttpVersion(version)) == expected_version


def test_http_version_parsing_with_error() -> None:
    with pytest.raises(InvalidHttpVersionError):
        HttpVersion("SomeIvalidHttpVersion")
