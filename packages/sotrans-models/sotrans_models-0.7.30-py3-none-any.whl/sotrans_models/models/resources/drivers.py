from datetime import datetime
from enum import Enum
from typing import Union

from mongo_path.meta import MongoMeta
from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber

from sotrans_models.models._base import BaseOIDModel, InsertByOIDModel
from sotrans_models.models._mongo import PydanticObjectId
from sotrans_models.models.misc.document import DocumentCreateModel, DocumentDBModel
from sotrans_models.models.misc.verification import VerificationDBModel
from sotrans_models.utils.make_partial_model import optional_fields_model


class DriverStatus(str, Enum):
    ready = "ready"
    on_the_way = "on_the_way"
    blocked = "blocked"


# Drivers license models


class DriversLicenseModel(BaseModel):
    number: str
    country: str
    valid_from: datetime
    valid_to: datetime
    issued_by: str


# Drivers passport models


class PassportModel(BaseModel):
    series: str
    number: str
    issue_date: datetime
    issued_by: str
    birthdate: datetime
    birthplace: str
    registration_address: str
    country: str


# Driver models


class DriverBaseModel(BaseModel):
    surname: str
    name: str
    patronymic: str | None = None
    status: DriverStatus = DriverStatus.ready
    inn: str
    photo: str | None = None
    phone: PhoneNumber | None = None
    note: str | None = None


class DriverCreateModel(DriverBaseModel):
    drivers_license: DriversLicenseModel
    passport: PassportModel
    documents: list[Union[InsertByOIDModel, DocumentCreateModel]] | None = None


@optional_fields_model
class DriverUpdateModel(DriverCreateModel):
    pass


class DriverDBModel(DriverUpdateModel, BaseOIDModel, metaclass=MongoMeta):
    verification: VerificationDBModel | None = None
    is_active: bool | None = None
    organization_id: PydanticObjectId = None
    documents: list[DocumentDBModel] | None = None
    created_at: datetime | None = None
