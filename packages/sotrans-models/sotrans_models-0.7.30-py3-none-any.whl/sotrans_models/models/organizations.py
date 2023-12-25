from datetime import datetime
from enum import Enum
from typing import List, Optional

from mongo_path.meta import MongoMeta

from sotrans_models.models._base import BaseOIDModel, InsertByOIDModel, InsertByUUIDModel
from sotrans_models.models.misc.document import DocumentCreateModel, DocumentDBModel
from sotrans_models.models.users import SotransUserDBModel
from sotrans_models.models.misc.verification import VerificationDBModel
from pydantic import BaseModel, field_validator


class InnVerificationStatus(str, Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class OrganizationBaseModel(BaseModel):
    head: str | None = None
    ownership_type: str | None = None
    logo: str | None = None

    legal_address: str | None = None
    factual_address: str | None = None
    phone: str | None = None
    email: str | None = None

    kpp: str | None = None
    ogrn: str | None = None
    taxation_type: str | None = None
    bank: str | None = None
    bik: str | None = None
    ifns_code: str | None = None
    registration_date: datetime | None = None
    contact_user: InsertByUUIDModel | None = None

    documents: List[InsertByOIDModel | DocumentCreateModel] | None = None


class OrganizationCreateModel(OrganizationBaseModel):
    inn: str

    @field_validator("inn")
    @classmethod
    def validate_inn(cls, v: str):
        try:
            int(v)
        except ValueError:
            raise ValueError("INN must be a number")
        if len(v) != 10 and len(v) != 12:
            raise ValueError("INN must be 10 or 12 digits")
        return v


class OrganizationUpdateModel(OrganizationBaseModel):
    inn: Optional[str] = None
    inn_verification_status: Optional[
        InnVerificationStatus
    ] = None  # Either success/failed/pending


class UpdateINNPayload(BaseModel):
    inn: str

    @field_validator("inn")
    @classmethod
    def validate_inn(cls, v: str):
        try:
            int(v)
        except ValueError:
            raise ValueError("INN must be a number")
        if len(v) != 10 and len(v) != 12:
            raise ValueError("INN must be 10 or 12 digits")
        return v


class OrganizationDBModel(OrganizationUpdateModel, BaseOIDModel, metaclass=MongoMeta):
    owner: SotransUserDBModel | None = None
    created_at: datetime | None = None
    is_active: bool | None = None
    inn_verification_status: InnVerificationStatus | None = (
        None  # Either success/failed/pending
    )
    full_verification: bool = False

    contact_user: SotransUserDBModel | None = None
    verification: VerificationDBModel | None = None
    documents: List[DocumentDBModel] | None = None
    employees: List[SotransUserDBModel] | None = None
