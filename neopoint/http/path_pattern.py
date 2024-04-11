import re

__all__ = [
    "PathPattern",
]


class PathPattern:
    """
    Hold information about path pattern, can match requested_path by given pattern.
    Transform patern '/users/{user_id}/posts/{post_id}' into re pattern '/users/([^/]+)/posts/.+'.

    Attributes
    ----------
    syntax_pattern : str
        hold a pattern in look like '/users/{user_id}'.
    re_pattern : re.Pattern
        already transformed syntax_pattern into regexp.
    """

    _syntax_pattern: str
    _re_pattern: re.Pattern

    def __init__(self, syntax_pattern: str) -> None:
        self._syntax_pattern = syntax_pattern
        self._re_pattern = self._get_re_pattern(syntax_pattern)

    def _get_re_pattern(self, syntax_pattern: str) -> re.Pattern:
        """Replace substrings like '{some_path_param_name}' to '([^/]+)'."""

        while "{" in syntax_pattern and "}" in syntax_pattern:
            reg_start = syntax_pattern.find("{")
            reg_end = syntax_pattern.find("}") + 1

            syntax_pattern = syntax_pattern[:reg_start] + r"([^/]+)" + syntax_pattern[reg_end:]

        return re.compile(syntax_pattern)

    def match(self, requested_path: str) -> re.Match | None:
        return self._re_pattern.fullmatch(requested_path)

    def append_prefix(self, prefix: str) -> None:
        self._syntax_pattern = prefix + self._syntax_pattern
        self._re_pattern = re.compile(prefix + self._re_pattern.pattern)

    @property
    def syntax_pattern(self) -> str:
        return self._syntax_pattern

    @property
    def re_pattern(self) -> re.Pattern:
        return self._re_pattern
