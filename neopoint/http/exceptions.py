__all__ = [
    "InvalidHeaderEncodingError",
    "InvalidHttpVersionError",
    "InvalidQueryStringError",
    "RequestInvalidContentTypeError",
]


class InvalidHeaderEncodingError(Exception):
    ...


class InvalidHttpVersionError(Exception):
    ...


class RequestInvalidContentTypeError(Exception):
    ...


class InvalidQueryStringError(Exception):
    ...
