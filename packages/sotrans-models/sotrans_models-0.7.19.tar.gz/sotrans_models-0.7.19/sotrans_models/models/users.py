from typing import Annotated, Any, Dict, List

from sotrans_fastapi_keycloak.role import Role

from sotrans_models.models._base import BaseUUIDModel
from pydantic import BaseModel, model_validator
from sotrans_fastapi_keycloak.model import (
    KeycloakUserAttribute,
    KeycloakUserBaseModel,
    OIDCUserBaseModel,
    user_model_attributes_serializer,
    user_model_attributes_validator,
)

from sotrans_models.models.roles import SotransRole, sotrans_roles
from sotrans_models.utils.constrained_pydantic_types import EmailString

KeycloakUserOptionalStrAttribute = Annotated[
    str | None, KeycloakUserAttribute()
]
KeycloakUserStrAttribute = Annotated[str, KeycloakUserAttribute()]


def get_highest_role(my_roles: List[SotransRole]) -> str:
    """
    Get the highest role in the hierarchy from a list of SotransRole enums.

    Args:
        my_roles (List[SotransRole]): List of SotransRole enums.

    Returns:
        SotransRole: The highest SotransRole enum in the hierarchy.
    """

    # Function to calculate the depth of a role in the hierarchy
    def role_depth(role: Role) -> int:
        depth = 0
        while role.ancestors:
            depth += 1
            role = role.ancestors[0]  # assuming one ancestor for simplicity
        return depth

    # Convert SotransRole enums to Role objects
    role_objects = [sotrans_roles[role] for role in my_roles]

    # Sort the Role objects based on their depth in the hierarchy
    sorted_roles = sorted(role_objects, key=role_depth, reverse=True)

    # Find the corresponding SotransRole for the highest Role object
    if sorted_roles:
        for key, value in sotrans_roles.items():
            if value == sorted_roles[0]:
                return key

    return ""


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



class SotransOIDCUserModel(OIDCUserBaseModel, SotransKeycloakUserInfoModel):
    pass


class SotransUserDBModel(BaseUUIDModel, SotransKeycloakUserInfoModel):
    pass


class UpdateRoleModel(BaseModel):
    role: SotransRole
