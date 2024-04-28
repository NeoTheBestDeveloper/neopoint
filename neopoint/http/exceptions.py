from typing import Final

from .http_status import HttpStatus

__all__ = [
    "InvalidHeaderEncodingError",
    "InvalidHttpVersionError",
    "InvalidQueryStringError",
    "RequestInvalidContentTypeError",
    "ValidationError",
    "MissedRequiredQueryParamError",
    "InvalidTypeForQueryParamError",
]


class ValidationError(Exception):
    status: Final[HttpStatus]
    msg: Final[str]

    def __init__(self, msg: str, status: HttpStatus) -> None:
        super().__init__(msg)

        self.msg = msg
        self.status = status


class MissedRequiredQueryParamError(ValidationError):
    def __init__(self, param_name: str) -> None:
        super().__init__(
            f"Expected to get required query parameter '{param_name}', but it missed.",
            HttpStatus.HTTP_422_UNPROCESSABLE_CONTENT,
        )


class InvalidTypeForQueryParamError(ValidationError):
    def __init__(self, param_name: str, expected_type: type, gotten_type: type) -> None:
        super().__init__(
            f"Parameter '{param_name}' has invalid type. Expected {expected_type}, but gotten {gotten_type}",
            HttpStatus.HTTP_422_UNPROCESSABLE_CONTENT,
        )


class InvalidHeaderEncodingError(Exception):
    ...


class InvalidHttpVersionError(Exception):
    ...


class RequestInvalidContentTypeError(Exception):
    ...


class InvalidQueryStringError(Exception):
    ...
