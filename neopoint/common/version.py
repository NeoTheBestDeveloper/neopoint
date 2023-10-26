from dataclasses import dataclass

__all__ = [
    "Version",
]


@dataclass(frozen=True, slots=True)
class Version:
    major: int
    minor: int
