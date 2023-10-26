__all__ = [
    "InvalidHeaderEncodingError",
    "InvalidHttpVersionError",
    "RequestInvalidContentTypeError",
]


class InvalidHeaderEncodingError(Exception):
    ...


class InvalidHttpVersionError(Exception):
    ...


class RequestInvalidContentTypeError(Exception):
    ...
