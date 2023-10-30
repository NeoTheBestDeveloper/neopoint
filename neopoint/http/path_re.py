import re

__all__ = [
    "PathRe",
]


class PathRe:
    _path_re_pattern: re.Pattern
    _path_pattern: str

    def __init__(self, path_pattern: str) -> None:
        self._path_pattern = path_pattern
        self._path_re_pattern = self._get_re_pattern(path_pattern)

    def _get_re_pattern(self, path_pattern: str) -> re.Pattern:
        while "{" in path_pattern and "}" in path_pattern:
            reg_start = path_pattern.find("{")
            reg_end = path_pattern.find("}") + 1

            path_pattern = path_pattern[:reg_start] + r"(.+)" + path_pattern[reg_end:]

        return re.compile(path_pattern)

    def match(self, requested_path: str) -> re.Match | None:
        return self._path_re_pattern.fullmatch(requested_path)

    def append_prefix(self, prefix: str) -> None:
        self._path_pattern = prefix + self._path_pattern
        self._path_re_pattern = re.compile(prefix + self._path_re_pattern.pattern)

    @property
    def path_pattern(self) -> str:
        return self._path_pattern

    @property
    def path_re_pattern(self) -> re.Pattern:
        return self._path_re_pattern
