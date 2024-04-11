import json as json_lib
from typing import Any

from .http_status import HttpStatus
from .message import Message

__all__ = [
    "Response",
    "TextResponse",
    "HtmlResponse",
    "JsonResponse",
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

    @property
    def headers(self) -> dict[str, str]:
        return self._headers


class TextResponse(Response):
    def __init__(
        self,
        text: str,
        status: HttpStatus = HttpStatus.HTTP_200_OK,
        headers: dict[str, str] | None = None,
    ) -> None:
        content = text.encode(self._charset)

        super().__init__(
            status=status,
            content=content,
            headers=headers,
            media_type="text/plain",
        )


class HtmlResponse(Response):
    def __init__(
        self,
        template_name: str,
        status: HttpStatus = HttpStatus.HTTP_200_OK,
        headers: dict[str, str] | None = None,
    ) -> None:
        with open(f"templates/{template_name}") as template:
            content = template.read().encode(self._charset)

            super().__init__(
                status=status,
                content=content,
                headers=headers,
                media_type="text/html",
            )


class JsonResponse(Response):
    def __init__(
        self,
        json: Any,
        status: HttpStatus = HttpStatus.HTTP_200_OK,
        headers: dict[str, str] | None = None,
    ) -> None:
        content = json_lib.dumps(json).encode(self._charset)

        super().__init__(
            status=status,
            content=content,
            headers=headers,
            media_type="application/json",
        )
