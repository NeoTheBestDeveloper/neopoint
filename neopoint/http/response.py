from .http_status import HttpStatus
from .message import Message

__all__ = [
    "Response",
]


class Response(Message):
    _status: HttpStatus

    def __init__(
        self,
        status: HttpStatus,
        content: bytes | None = None,
        media_type: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._status = status
        super().__init__(
            content=content,
            headers=headers,
            media_type=media_type,
        )

    @property
    def status(self) -> HttpStatus:
        return self._status


class HtmlResponse(Response):
    def __init__(self, template_name: str) -> None:
        with open(f"templates/{template_name}") as template:
            payload = template.read().encode("utf-8")

            super().__init__(HttpStatus.HTTP_200_OK, payload, "text/html")
