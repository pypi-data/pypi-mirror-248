from mongo_path.meta import MongoMeta
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sotrans_fastapi_keycloak._uuid import PydanticUUID

from sotrans_models.models._base import BaseOIDModel, InsertByUUIDModel
from sotrans_models.models._mongo import PydanticObjectId
from sotrans_models.models.users import SotransUserDBModel
from sotrans_models.utils.make_partial_model import optional_fields_model


class ClientCreateModel(BaseModel):
    name: str
    short_name: str | None = None
    inn: str
    kpp: str | None = None
    ogrn: str
    legal_address: str
    actual_address: str
    phone: PhoneNumber
    email: EmailStr
    website: str | None = None

    bank: str | None = None
    bik: str | None = None
    checking_account: str | None = None
    correspondent_account: str | None = None

    # Думаю будет лучше и логичнее хранить подответственных КА у пользователя, чтобы быстрее осуществлять поиск по ним
    # Но здесь ссылки тоже нужны, чтобы управляющему быстро смотреть список ответственных пользователей
    responsible: list[InsertByUUIDModel] | None = None
    note: str | None = None


@optional_fields_model
class ClientUpdateModel(ClientCreateModel):
    pass


class ClientDBModel(ClientUpdateModel, BaseOIDModel, metaclass=MongoMeta):
    responsible: list[SotransUserDBModel] | None = None


class ManagersClientsCreateModel(BaseModel):
    manager_id: PydanticUUID
    clients_ids: list[PydanticObjectId]


class ManagersClientsDBModel(BaseOIDModel, ManagersClientsCreateModel, metaclass=MongoMeta):
    pass


class SubsidiaryClientResponse(BaseModel):
    subsidiary_id: PydanticObjectId
    clients_id: PydanticObjectId


class AssignedToClientResponse(BaseModel):
    client_id: PydanticObjectId
    employees_ids: list[PydanticUUID]
