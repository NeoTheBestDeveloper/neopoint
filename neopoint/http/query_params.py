import re
from typing import Any, Iterator, Mapping, NoReturn

from .exceptions import (
    InvalidQueryStringError,
    InvalidTypeForQueryParamError,
    MissedRequiredQueryParamError,
)

__all__ = [
    "QueryParams",
]

DECODE_TABLE: dict[str, str] = {
    "<": "%3C",
    ">": "%3E",
    "#": "%23",
    "%": "%25",
    "{": "%7B",
    "}": "%7D",
    "|": "%7C",
    "\\": "%5C",
    "^": "%5E",
    "~": "%7E",
    "[": "%5B",
    "]": "%5D",
    "`": "%60",
    ";": "%3B",
    "/": "%2F",
    "?": "%3F",
    ":": "%3A",
    "@": "%40",
    "=": "%3D",
    "&": "%26",
    "$": "%24",
    "+": "%2B",
    '"': "%22",
    " ": "%20",
}


class QueryParams(Mapping):
    _params: dict[str, str | list[str]]
    _pair_pattern: re.Pattern = re.compile(r"\w+=[\w\"']+")

    def __init__(self, query_string: str) -> None:
        self._params = {}

        if not query_string:
            return

        query_string = self._decode_query_string(query_string)

        if not self._validate_query_string(query_string):
            raise InvalidQueryStringError(f"Ivalid query string {query_string}.")

        self._parse_query_string(query_string)

    def validate_types(self, annotations: dict[str, Any], defaults: tuple[Any, ...]) -> None | NoReturn:
        for idx, name in enumerate(reversed(annotations)):
            if self._params.get(name, None) is None and len(defaults) <= idx:
                raise MissedRequiredQueryParamError(name)
            try:
                if self._params.get(name, None) is not None:
                    annotations[name](self._params[name])
            except ValueError:
                raise InvalidTypeForQueryParamError(name, annotations[name], type(self._params[name]))

        return None

    def _decode_query_string(self, query_string: str) -> str:
        for decoded, encoded in DECODE_TABLE.items():
            query_string = query_string.replace(encoded, decoded)

        return query_string

    def _parse_value(self, value: str) -> str | list[str]:
        return value.split(",") if "," in value else value

    def _extend_array_value(self, values_storage: list[str], parsed_value: str | list[str]) -> None:
        if isinstance(parsed_value, str):
            values_storage.append(parsed_value)
        else:
            values_storage.extend(parsed_value)

    def _init_array_value(self, key: str, prev_value: str, parsed_value: str | list[str]) -> None:
        if isinstance(parsed_value, str):
            self._params[key] = [prev_value, parsed_value]
        else:
            self._params[key] = [prev_value, *parsed_value]

    def _parse_key_value(self, key: str, value: str) -> None:
        parsed_value = self._parse_value(value)

        if self._params.get(key, None) is None:
            self._params[key] = parsed_value
        else:
            prev_value = self._params[key]

            if isinstance(prev_value, list):
                self._extend_array_value(prev_value, parsed_value)
            else:
                self._init_array_value(key, prev_value, parsed_value)

    def _parse_query_string(self, query_string: str) -> None:
        for param in query_string.split("&"):
            key, value = param.split("=")
            self._parse_key_value(key, value)

    def _validate_query_string(self, query_string: str) -> bool:
        if "&" in query_string:
            return all(self._pair_pattern.match(pair) for pair in query_string.split("&"))

        return self._pair_pattern.match(query_string) is not None

    def __getitem__(self, __name: str) -> str | list[str]:
        return self._params[__name]

    def __len__(self) -> int:
        return len(self._params)

    def __iter__(self) -> Iterator[str]:
        return iter(self._params)

    def __bool__(self) -> bool:
        return bool(self._params)
