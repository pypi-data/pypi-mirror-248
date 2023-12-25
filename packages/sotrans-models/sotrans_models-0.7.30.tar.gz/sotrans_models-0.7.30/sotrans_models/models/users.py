from typing import Annotated, Any, List

from sotrans_models.models._base import BaseUUIDModel
from pydantic import BaseModel, model_validator
from sotrans_fastapi_keycloak.model import (
    KeycloakUserAttribute,
    KeycloakUserBaseModel,
    OIDCUserBaseModel,
    user_model_attributes_serializer,
    user_model_attributes_validator,
)

from sotrans_models.models.roles import SotransRole
from sotrans_models.utils.constrained_pydantic_types import EmailString

KeycloakUserOptionalStrAttribute = Annotated[
    str | None, KeycloakUserAttribute()
]
KeycloakUserStrAttribute = Annotated[str, KeycloakUserAttribute()]


class SotransKeycloakUserBaseModel(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def validate(cls: type[BaseModel], value: Any) -> Any:
        return user_model_attributes_validator(cls, value)

    def model_dump_keycloak(self):
        return user_model_attributes_serializer(self)


class SotransKeycloakUserInfoModel(SotransKeycloakUserBaseModel):
    """Represents a Keycloak user info object in SOTRANS configuration"""

    email: KeycloakUserOptionalStrAttribute = None
    name: KeycloakUserOptionalStrAttribute = None
    surname: KeycloakUserOptionalStrAttribute = None
    patronymic: KeycloakUserOptionalStrAttribute = None
    phone: KeycloakUserOptionalStrAttribute = None
    job_title: KeycloakUserOptionalStrAttribute = None
    status: KeycloakUserOptionalStrAttribute = None
    photo: KeycloakUserOptionalStrAttribute = None
    subsidiary_id: KeycloakUserOptionalStrAttribute = None
    organization_id: KeycloakUserOptionalStrAttribute = None
    policy: KeycloakUserOptionalStrAttribute = None
    note: KeycloakUserOptionalStrAttribute = None
    username: KeycloakUserOptionalStrAttribute = None


class SotransKeycloakUserUpdateModel(SotransKeycloakUserBaseModel):
    """Represents a Keycloak user info object in SOTRANS configuration"""

    email: KeycloakUserOptionalStrAttribute = None
    name: KeycloakUserOptionalStrAttribute = None
    surname: KeycloakUserOptionalStrAttribute = None
    patronymic: KeycloakUserOptionalStrAttribute = None
    phone: KeycloakUserOptionalStrAttribute = None
    job_title: KeycloakUserOptionalStrAttribute = None
    status: KeycloakUserOptionalStrAttribute = None
    photo: KeycloakUserOptionalStrAttribute = None
    subsidiary_id: KeycloakUserOptionalStrAttribute = None
    policy: KeycloakUserOptionalStrAttribute = None
    note: KeycloakUserOptionalStrAttribute = None


class SotransKeycloakUserPublicUpdateModel(SotransKeycloakUserBaseModel):
    """Represents an update Keycloak user object in SOTRANS configuration"""

    email: KeycloakUserOptionalStrAttribute = None
    name: KeycloakUserOptionalStrAttribute = None
    surname: KeycloakUserOptionalStrAttribute = None
    patronymic: KeycloakUserOptionalStrAttribute = None
    phone: KeycloakUserOptionalStrAttribute = None
    photo: KeycloakUserOptionalStrAttribute = None


class SotransKeycloakUserCreateModel(SotransKeycloakUserBaseModel):
    """Represents a creation Keycloak user object in SOTRANS configuration"""

    name: KeycloakUserStrAttribute
    surname: KeycloakUserStrAttribute
    patronymic: KeycloakUserStrAttribute
    phone: KeycloakUserStrAttribute
    organization_id: KeycloakUserOptionalStrAttribute = None
    email: KeycloakUserOptionalStrAttribute
    password: str


class SotransKeycloakUserCreateModelWithMinioPolicy(
    SotransKeycloakUserCreateModel
):
    """Represents a creation Keycloak user object with addition of required minio policy attribute"""

    policy: KeycloakUserStrAttribute


class SotransKeycloakUserModel(
    KeycloakUserBaseModel, SotransKeycloakUserInfoModel
):
    """Represents a full Keycloak user object in SOTRANS configuration"""

    # These fields are computed and loaded on fly in main-service
    roles: List[str] = []
    role: str = ""


class SotransOIDCUserModel(OIDCUserBaseModel, SotransKeycloakUserInfoModel):
    pass


class SotransUserDBModel(BaseUUIDModel, SotransKeycloakUserInfoModel):
    pass


class UpdateRoleModel(BaseModel):
    role: SotransRole
