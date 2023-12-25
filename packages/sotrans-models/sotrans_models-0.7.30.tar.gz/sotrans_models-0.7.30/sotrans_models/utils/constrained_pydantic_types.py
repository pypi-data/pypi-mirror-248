from typing import Annotated

from pydantic import Field

EmailString = Annotated[
    str,
    Field(
        pattern=r"^[\w\.\-]+@([\w-]+\.)+[\w-]{2,4}$",
        examples=[
            "test@mail.ru",
        ],
    ),
]
