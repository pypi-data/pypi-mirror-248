from mongo_path.meta import MongoMeta

from sotrans_models.models.resources.trucks import (
    TruckType,
    VehicleCreateBaseModel,
    VehicleDBBaseModel,
    VehicleUpdateBaseModel,
)


class TrailerCreateModel(VehicleCreateBaseModel):
    truck_type: TruckType | None = None


class TrailerUpdateModel(VehicleUpdateBaseModel):
    truck_type: TruckType | None = None


class TrailerDBModel(VehicleDBBaseModel, metaclass=MongoMeta):
    pass
