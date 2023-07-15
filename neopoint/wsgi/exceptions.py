__all__ = ("UnsupportedProtocol",)


class UnsupportedProtocol(Exception):
    """Raise if environ wsg.url_schema is not 'http' or 'https'"""
