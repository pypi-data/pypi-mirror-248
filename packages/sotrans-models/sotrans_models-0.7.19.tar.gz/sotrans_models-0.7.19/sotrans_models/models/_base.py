# mypy: disable-error-code="arg-type, index, operator"
import warnings
from typing import Any, Literal, get_args
from uuid import UUID, uuid4

import typing_extensions
from bson import ObjectId

from sotrans_models.models._mongo import PydanticObjectId
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo

# from pydantic.main import IncEx
from sotrans_fastapi_keycloak._uuid import PydanticUUID
from sotrans_models.utils.type_checks import is_list, is_model, is_not_generic_alias, is_union

warnings.filterwarnings('ignore', category=UserWarning)

IncEx: typing_extensions.TypeAlias = (
    "set[int] | set[str] | dict[int, Any] | dict[str, Any] | None"
)


def format_if_id(o: object, field_type: type):
    """
    Recursive function that scans all parameters annotations in-depth to format all
    ObjectId and UUID fields to corresponding types.

    :param o: parameter object to scan and format
    :param field_type: parameter annotation type
    :return:
    """
    if not o:
        return o

    if is_union(field_type):
        for c in get_args(field_type):
            o = format_if_id(o, c)
    elif is_list(field_type, o):
        for i in range(len(o)):
            for c in get_args(field_type):
                o[i] = format_if_id(o[i], c)
    elif is_not_generic_alias(field_type):
        if is_model(field_type, o):
            for field_name, field_info in field_type.model_fields.items():
                if field_name not in o:
                    continue
                o[field_name] = format_if_id(
                    o[field_name], field_info.annotation
                )
        elif issubclass(field_type, ObjectId) and isinstance(o, str):
            o = ObjectId(o)
        elif issubclass(field_type, UUID) and isinstance(o, str):
            o = UUID(o)
    else:
        print(f"Unhandled annotation yet {field_type}")

    return o


def analyse_and_replace_ids(dump: dict, model_fields: dict[str, FieldInfo]):
    for field_name, field_info in model_fields.items():
        if field_name not in dump:
            continue
        dump[field_name] = format_if_id(
            dump[field_name], field_info.annotation
        )


class BaseIdModel(BaseModel):
    # def default_model_dump(
    #         self,
    #         *,
    #         mode: Literal["json", "python"] | str = "python",
    #         include: IncEx = None,
    #         exclude: IncEx = None,
    #         by_alias: bool = False,
    #         exclude_unset: bool = False,
    #         exclude_defaults: bool = False,
    #         exclude_none: bool = False,
    #         round_trip: bool = False,
    #         warnings: bool = True
    # ) -> dict[str, Any]:
    #     dump = super(BaseIdModel, self).model_dump(
    #         mode=mode,
    #         include=include,
    #         exclude=exclude,
    #         by_alias=by_alias,
    #         exclude_unset=exclude_unset,
    #         exclude_defaults=exclude_defaults,
    #         exclude_none=exclude_none,
    #         round_trip=round_trip,
    #         warnings=warnings,
    #     )
    #
    #
    #     return dump

    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
        format_ids: bool = True,
    ) -> dict[str, Any]:
        dump = super(BaseIdModel, self).model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )
        if format_ids:
            analyse_and_replace_ids(dump, self.model_fields)

        return dump


class InsertByOIDModel(BaseIdModel):
    id: PydanticObjectId = Field(serialization_alias="_id")


class BaseOIDModel(BaseIdModel):
    id: PydanticObjectId = Field(None)


class InsertByUUIDModel(BaseIdModel):
    id: PydanticUUID = Field()


class BaseUUIDModel(BaseIdModel):
    id: PydanticUUID = Field(None)


def test_uuid():
    from_db = {"id": uuid4()}
    # from_db = {"_id": ObjectId()}
    # from_api = {"id": str(ObjectId())}
    from_api = {"id": str(uuid4())}

    m = BaseUUIDModel(**from_db)
    assert isinstance(m.id, UUID)
    print(m.model_dump())
    print(m.model_dump(by_alias=True))
    print(m.model_dump_json())

    m = InsertByUUIDModel(**from_api)
    assert isinstance(m.id, UUID)
    print(m.model_dump())
    print(m.model_dump(by_alias=True))
    print(m.model_dump_json())

test_uuid()