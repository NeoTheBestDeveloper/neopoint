from typing import NoReturn

from .exceptions import InvalidHeaderEncodingError

__all__ = [
    "Message",
]


class Message:
    "Describes base http message."

    _charset: str = "utf-8"
    _headers_encoding: str = "latin-1"

    _headers: dict[str, str]
    _content: bytes
    _media_type: str = "application/octet-stream"

    def __init__(
        self, content: bytes | str | None, headers: dict[str, str] | None = None, media_type: str | None = None
    ) -> None:
        if headers is not None:
            self._validate_headers(headers)

        self._headers = {} if headers is None else headers.copy()
        self._content = self._content_to_bytes(content)

        if media_type is not None:
            self._media_type = media_type

        if self._content:
            content_type = self._media_type
            if content_type.startswith("text/"):
                content_type += f"; charset={self._charset}"

            self._headers["Content-Type"] = content_type
            self._headers["Content-Length"] = str(len(self._content))

    def _content_to_bytes(self, content: bytes | str | None) -> bytes:
        if content is None:
            return b""

        if isinstance(content, str):
            return content.encode(self._charset)

        return content

    def _can_encode(self, string: str) -> bool:
        try:
            string.encode(self._headers_encoding)
            return True
        except UnicodeEncodeError:
            return False

    def _validate_headers(self, headers: dict[str, str]) -> None | NoReturn:
        for k, v in headers.items():
            if not (self._can_encode(k) and self._can_encode(v)):
                raise InvalidHeaderEncodingError(
                    "Keys and values for http headers must contains only symbol,"
                    f"which can be encoded with '{self._headers_encoding}'"
                )
        return None

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def media_type(self) -> str:
        return self._media_type
