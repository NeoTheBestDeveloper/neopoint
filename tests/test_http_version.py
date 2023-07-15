from dataclasses import astuple

import pytest

from neopoint.http import HttpVersion


@pytest.mark.parametrize(
    "version,expected_version",
    [
        ("HTTP/1.1", (1, 1)),
        ("HTTP/2", (2, 0)),
        ("HTTP/3", (3, 0)),
    ],
)
def test_http_version_parsing(version: str, expected_version: tuple[int, int]):
    assert astuple(HttpVersion(version)) == expected_version
