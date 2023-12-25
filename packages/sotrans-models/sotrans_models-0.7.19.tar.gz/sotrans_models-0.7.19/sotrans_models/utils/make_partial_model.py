from copy import deepcopy
from typing import Any, Optional, Set

from pydantic import BaseModel, ConfigDict, create_model
from pydantic.fields import FieldInfo


def optional_fields_model(
    model: type[BaseModel] | None = None,
    *,
    fields_to_exclude: Set[str] | None = None,
    fields_to_ignore: Set[str] | None = None
):
    if fields_to_exclude is None:
        fields_to_exclude = set()
    if fields_to_ignore is None:
        fields_to_ignore = set()

    def inner(_model: type[BaseModel]):
        def field_info_tuple(field_info):
            return field_info.annotation, field_info

        def make_field_optional(
            field: FieldInfo, default: Any = None
        ) -> tuple[Any, FieldInfo]:
            new = deepcopy(field)
            new.default = default
            new.annotation = Optional[field.annotation]
            return field_info_tuple(new)

        fields: dict[str, tuple[type, FieldInfo]] = {}
        for field_name, field_info in _model.model_fields.items():
            if field_name not in fields_to_exclude:
                fields[field_name] = (
                    field_info_tuple(field_info)
                    if field_name in fields_to_ignore
                    else make_field_optional(field_info)
                )

        return create_model(
            _model.__name__, __module__=_model.__module__, **fields
        )

    return inner if model is None else inner(model)
