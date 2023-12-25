from collections.abc import Callable
from typing import Annotated, Any

from bson import ObjectId
from fastapi import Path, Query
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class _PydanticObjectIdAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.union_schema(
                    [core_schema.str_schema(), core_schema.none_schema()]
                ),
                core_schema.no_info_plain_validator_function(
                    validate_from_str
                ),
            ],
            # serialization=core_schema.plain_serializer_function_ser_schema(
            #     lambda instance: str(instance)
            # ),
        )
        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.union_schema(
                        [
                            core_schema.is_instance_schema(ObjectId),
                            core_schema.none_schema(),
                        ]
                    ),
                    from_str_schema,
                ],
                # serialization=core_schema.plain_serializer_function_ser_schema(
                #     lambda instance: PydanticObjectId(instance)
                # ),
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance) if instance else None
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


PydanticObjectId = Annotated[ObjectId, _PydanticObjectIdAnnotation]
PydanticObjectIdPath = Annotated[PydanticObjectId, Path()]
PydanticObjectIdQuery = Annotated[PydanticObjectId, Query()]
