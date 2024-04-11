from typing import NoReturn

from ..common import Version
from .exceptions import InvalidHttpVersionError

__all__ = [
    "HttpVersion",
]


class HttpVersion(Version):
    def __init__(self, version: str) -> None:
        self._validate_version(version)

        sub_version_indetifiers = version.split("/")[1].split(".")
        major = int(sub_version_indetifiers[0])
        minor = 0 if len(sub_version_indetifiers) == 1 else int(sub_version_indetifiers[1])

        super().__init__(major, minor)

    def _validate_version(self, version: str) -> None | NoReturn:
        supported_versions = ("HTTP/1.0", "HTTP/1.1", "HTTP/2", "HTTP/3")

        if version not in supported_versions:
            raise InvalidHttpVersionError
        return None
