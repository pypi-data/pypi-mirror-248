from types import GenericAlias, UnionType
from typing import (  # type: ignore[attr-defined]
    Union,
    _GenericAlias,
    get_origin,
)

from pydantic import BaseModel  # type: ignore[import-not-found]


def is_union(o: object) -> bool:
    origin = get_origin(o)
    return origin is Union or origin is UnionType


def is_list_type(field_type: type) -> bool:
    return get_origin(field_type) is list


def is_list(cls: type, o: object) -> bool:
    return is_list_type(cls) and isinstance(o, list)


def is_not_generic_alias(cls: type) -> bool:
    return not isinstance(cls, GenericAlias) and not isinstance(
        cls, _GenericAlias
    )


def is_model(cls: type, o: object) -> bool:
    return issubclass(cls, BaseModel) and isinstance(o, dict)
