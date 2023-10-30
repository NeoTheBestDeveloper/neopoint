from typing import Iterator, Mapping

from .path_re import PathRe

__all__ = [
    "PathParams",
]


class PathParams(Mapping):
    """Get path params from requested path. Use it only if requested_path is match path_pattern."""

    _params: dict[str, str]

    def __init__(self, requested_path: str, path_pattern: PathRe) -> None:
        params_names = self._get_params_names(path_pattern)
        params = self._get_params(requested_path, path_pattern)

        self._params = dict(zip(params_names, params))

    def _get_params_names(self, path_pattern: PathRe) -> tuple[str, ...]:
        match_res = path_pattern.match(path_pattern.path_pattern)

        if match_res is None:
            return tuple()

        return tuple(res.replace("{", "").replace("}", "") for res in match_res.groups())

    def _get_params(self, requested_path: str, path_pattern: PathRe) -> tuple[str, ...]:
        match_res = path_pattern.match(requested_path)
        if match_res is None:
            return tuple()

        return match_res.groups()

    def __getitem__(self, __name: str) -> str:
        return self._params[__name]

    def __len__(self) -> int:
        return len(self._params)

    def __iter__(self) -> Iterator[str]:
        return iter(self._params)

    def __bool__(self) -> bool:
        return bool(self._params)
