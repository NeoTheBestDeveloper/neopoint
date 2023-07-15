__all__ = ("Version",)


from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Version:
    major: int
    minor: int
