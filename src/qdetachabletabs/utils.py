from typing import TypeVar, cast

T = TypeVar("T")


def some(obj: T | None) -> T:
    "Casts an object to its type ignoring `None`."
    return cast(T, obj)
