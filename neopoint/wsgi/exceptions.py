__all__ = [
    "UnsupportedProtocolError",
]


class UnsupportedProtocolError(Exception):
    """Raise if environ wsgi.url_schema is not 'http' or 'https'"""
