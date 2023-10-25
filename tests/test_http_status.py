import pytest

from neopoint.http import HttpStatus


@pytest.mark.parametrize(
    "status,expected_status_code,expected_status_msg",
    [
        (HttpStatus.HTTP_200_OK, 200, "Ok"),
        (HttpStatus.HTTP_404_NOT_FOUND, 404, "Not Found"),
        (HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, 500, "Internal Server Error"),
    ],
)
def test_http_status(status: HttpStatus, expected_status_code: int, expected_status_msg: str) -> None:
    assert status.status_code == expected_status_code
    assert status.status_msg == expected_status_msg
