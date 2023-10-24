from dataclasses import dataclass

__all__ = [
    "TestResponse",
]


@dataclass(slots=True, frozen=True)
class TestResponse:
    status_code: int
    content: bytes
    headers: dict[str, str]
