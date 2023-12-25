from datetime import datetime
from enum import Enum
from typing import Union

from mongo_path.meta import MongoMeta
from pydantic import BaseModel, model_validator

from sotrans_models.models._base import BaseOIDModel, InsertByOIDModel
from sotrans_models.models._mongo import PydanticObjectId
from sotrans_models.models.misc.document import DocumentCreateModel, DocumentDBModel
from sotrans_models.models.misc.verification import VerificationDBModel
from sotrans_models.utils.make_partial_model import optional_fields_model


class BodyType(str, Enum):
    tilt = "tilt"  # тентованный
    refrigerator = "refrigerator"
    isotherm = "isotherm"


class LoadingType(str, Enum):
    side = "side"
    back = "back"
    top = "top"
    any = "any"

    # @property
    # def any_load(self):
    #     return [v for k, v in self.__dict__.items() if k[:1] != "_"]


class TruckType(str, Enum):
    van_truck = "van_truck"  # грузовик фургон
    tractor_unit = "tractor_unit"  # седельный тягач


class OwnershipType(str, Enum):
    own = "own"
    lease = "lease"


class TruckStatus(str, Enum):
    ready = "ready"
    on_the_way = "on_the_way"
    under_repair = "under_repair"
    blocked = "blocked"


class BodySettingsModel(BaseModel):
    body_type: list[BodyType]
    loading_type: list[LoadingType] | None = None
    weight: float | None = None
    volume: int | None = None

    @model_validator(mode='before')
    def validate_types(cls, data):
        if isinstance(data, dict):
            if 'body_type' in data and isinstance(data['body_type'], str):
                data['body_type'] = [data['body_type']]
            if 'loading_type' in data and isinstance(data['loading_type'], str):
                data['loading_type'] = [data['loading_type']]
        return data


class VehicleCreateBaseModel(BaseModel):
    registration_country: str
    brand: str | None = None
    model: str | None = None
    license_plate: str
    sts_number: str
    registration_date: datetime | None = None
    vin_number: str | None = None
    ownership_type: OwnershipType
    body: BodySettingsModel
    status: TruckStatus = TruckStatus.ready
    note: str | None = None
    documents: list[Union[InsertByOIDModel, DocumentCreateModel]] | None = None


@optional_fields_model
class VehicleUpdateBaseModel(VehicleCreateBaseModel):
    pass


class VehicleDBBaseModel(VehicleUpdateBaseModel, BaseOIDModel):
    verification: VerificationDBModel | None = None
    is_active: bool | None = None
    documents: list[DocumentDBModel] | None = None
    organization_id: PydanticObjectId = None
    created_at: datetime | None = None


class TruckCreateModel(VehicleCreateBaseModel):
    truck_type: TruckType


@optional_fields_model
class TruckUpdateModel(TruckCreateModel):
    pass


class TruckDBModel(VehicleDBBaseModel, metaclass=MongoMeta):
    truck_type: TruckType | None = None
