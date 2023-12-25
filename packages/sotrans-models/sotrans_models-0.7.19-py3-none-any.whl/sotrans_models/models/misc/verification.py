from enum import Enum

from mongo_path.meta import MongoMeta
from pydantic import BaseModel
from sotrans_fastapi_keycloak._uuid import PydanticUUID

from sotrans_models.models._base import BaseOIDModel
from sotrans_models.models._mongo import PydanticObjectId
from sotrans_models.utils.make_partial_model import optional_fields_model


class VerificationStatus(str, Enum):
    accepted = "accepted"
    declined = "declined"


class VerificationIssuerType(str, Enum):
    director = "director"
    security_service = "security_service"


class VerificationCreateModel(BaseModel):
    status: VerificationStatus
    issuer_type: VerificationIssuerType
    object_id: PydanticObjectId
    collection: str


# Used only in VerificationDBModel because BaseOIDModel and optional_fields_model are not compatible. Otherwise redundant
@optional_fields_model
class VerificationUpdateModel(VerificationCreateModel):
    pass


class VerificationDBModel(VerificationUpdateModel, BaseOIDModel, metaclass=MongoMeta):
    owner_id: PydanticUUID | None = None
