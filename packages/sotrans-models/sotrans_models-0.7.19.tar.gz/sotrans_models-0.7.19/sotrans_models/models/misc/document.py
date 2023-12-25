import datetime
from enum import Enum

from mongo_path.meta import MongoMeta
from pydantic import BaseModel

from sotrans_models.models._base import BaseOIDModel
from sotrans_models.models._mongo import PydanticObjectId
from sotrans_models.models.misc.verification import VerificationDBModel
from sotrans_models.utils.make_partial_model import optional_fields_model


class DriverDocumentType(str, Enum):
    drivers_license = "drivers_license"
    passport = "passport"


class TruckDocumentType(str, Enum):
    sts = "truck_sts"
    lease_contract = "truck_lease_contract"


class TrailerDocumentType(str, Enum):
    sts = "trailer_sts"

    lease_contract = "trailer_lease_contract"


class OrganizationDocumentType(str, Enum):
    company_charter = "company_charter"
    registration_certificate = "registration_certificate"


class RequestDocumentType(str, Enum):
    order_request = "order_request"


DocumentTypingAlias = (
    RequestDocumentType
    | OrganizationDocumentType
    | TruckDocumentType
    | TrailerDocumentType
    | DriverDocumentType
)


class DocumentTypeModel(BaseModel):
    document_type: DocumentTypingAlias


class DocumentStatus(str, Enum):
    final = "final"
    draft = "draft"


class DocumentCreateModel(BaseModel):
    type: DocumentTypingAlias
    link: str

    name: str | None = None
    number: str | None = None
    valid_until: datetime.datetime | None = None
    status: DocumentStatus = DocumentStatus.final
    note: str | None = None
    # Must be included if document is created independently
    object_id: PydanticObjectId | None = None
    collection: str | None = None


@optional_fields_model
class DocumentUpdateModel(DocumentCreateModel):
    pass


class DocumentDBModel(DocumentUpdateModel, BaseOIDModel, metaclass=MongoMeta):
    created_at: datetime.datetime | None = None
    verification: VerificationDBModel | None = None
    organization_id: PydanticObjectId | None = None
    deleted_at: datetime.datetime | None = None
