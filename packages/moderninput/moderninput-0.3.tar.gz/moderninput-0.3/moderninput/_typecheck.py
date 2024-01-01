from typing import get_args
from typing import Any
from types import UnionType


def type_check(value: Any, name: str, types: UnionType) -> Any:
    if Any not in get_args(tp=types) and not isinstance(value, types):
        raise ValueError(
            "{} must be {}, got '{}'".format(name, ", ".join(get_args(tp=types))),
            type(value).__name__,
        )

    return value
