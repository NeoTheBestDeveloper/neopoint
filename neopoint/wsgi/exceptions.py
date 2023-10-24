__all__ = ("UnsupportedProtocol",)


class UnsupportedProtocol(Exception):
    """Raise if environ wsgi.url_schema is not 'http' or 'https'"""
