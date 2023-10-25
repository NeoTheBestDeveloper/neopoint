from .http_status import HttpStatus

__all__ = [
    "Response",
]


class Response:
    _headers: dict[str, str]
    _content_type: str
    _payload: bytes
    _status: HttpStatus

    def __init__(
        self,
        status: HttpStatus,
        payload: bytes,
        content_type: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._headers = headers.copy() if headers else {}
        self._payload = payload
        self._content_type = content_type
        self._status = status

    @property
    def wsgi_normalized_headers(self) -> list[tuple[str, str]]:
        """Return normalized headers for WSGI protocol."""
        normalized_headers = list(self._headers.items())
        normalized_headers.append(("Content-type", self._content_type))
        normalized_headers.append(("Content-Length", str(len(self._payload))))

        return normalized_headers

    @property
    def wsgi_normalized_status(self) -> str:
        """Return normalized status for WSGI protocol."""
        return f"{self._status.status_code} {self._status.status_msg}"

    @property
    def payload(self) -> bytes:
        return self._payload


class HtmlResponse(Response):
    def __init__(self, template_name: str) -> None:
        with open(f"templates/{template_name}") as template:
            payload = template.read().encode("utf-8")

            super().__init__(HttpStatus.HTTP_200_OK, payload, "text/html; charset=utf-8")
