from ..utils import Version

__all__ = ("HttpVersion",)


class HttpVersion(Version):
    def __init__(self, version: str) -> None:
        sub_version_indetifiers = version.split("/")[1].split(".")
        major = int(sub_version_indetifiers[0])
        minor = 0 if len(sub_version_indetifiers) == 1 else int(sub_version_indetifiers[1])

        super().__init__(major, minor)
