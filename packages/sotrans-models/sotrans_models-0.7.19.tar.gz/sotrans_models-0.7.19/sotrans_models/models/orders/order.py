from datetime import datetime
from enum import Enum
from typing import Union

from mongo_path.meta import MongoMeta

from sotrans_models.models.orders.bid import BidDBModel

try:
    from config import DEFAULT_RATE_STEP
except ImportError:
    DEFAULT_RATE_STEP = 1000
from sotrans_models.models._base import BaseOIDModel, InsertByOIDModel, InsertByUUIDModel
from sotrans_models.models._mongo import PydanticObjectId
from sotrans_models.models.misc.client import ClientCreateModel, ClientDBModel
from sotrans_models.models.misc.document import DocumentCreateModel, DocumentDBModel
from sotrans_models.models.resources.drivers import DriverDBModel
from sotrans_models.models.organizations import OrganizationDBModel
from sotrans_models.models.resources.trailers import TrailerDBModel
from sotrans_models.models.resources.trucks import BodySettingsModel, TruckDBModel
from sotrans_models.models.users import SotransUserDBModel
from pydantic import BaseModel
from sotrans_models.utils.make_partial_model import optional_fields_model


class StopType(str, Enum):
    loading = "loading"
    unloading = "unloading"


class StageName(str, Enum):
    accepted = "accepted"
    finished = "finished"
    canceled = "canceled"
    stopped = "stopped"


class StageNameRequest(BaseModel):
    stage: StageName


class StopModel(BaseModel):
    index: int | None = None
    datetime: datetime
    address: str
    stop_type: StopType


class StopStage(BaseModel):
    stop_index: int | None = None


class OrderStageModel(BaseModel):
    type: StageName
    created_at: datetime
    stop: StopModel | None = None


class OrderStatus(str, Enum):
    """
    The flow is: buffer -> exchange [-> reserved ]->
    confirmed -> unverified -> active

    Can be archived at any time.
    """

    buffer = "buffer"
    appointment = "appointment"
    exchange = "exchange"
    reserved = "reserved"
    unverified = "unverified"
    confirmed = "confirmed"
    active = "active"
    archived = "archived"


class OrderExternalData(BaseModel):
    id: str | None = None
    url: str | None = None


class OrderBaseModel(BaseModel):
    auction_end_time: datetime
    stops: list[StopModel]
    cargo_type: str | None = None
    truck_body: BodySettingsModel
    value: int
    rate_step: int = DEFAULT_RATE_STEP
    status: OrderStatus = OrderStatus.buffer
    note: str | None = None
    external: OrderExternalData | None = None


class OrderCreateModel(OrderBaseModel):
    client: InsertByOIDModel | ClientCreateModel
    subsidiary_id: InsertByOIDModel | None = None
    company_logistician: InsertByUUIDModel | None = None
    carrier: InsertByOIDModel | None = None
    driver: InsertByOIDModel | None = None
    truck: InsertByOIDModel | None = None
    trailer: InsertByOIDModel | None = None
    documents: list[Union[InsertByOIDModel, DocumentCreateModel]] | None = None


@optional_fields_model
class OrderUpdateModel(OrderCreateModel):
    pass


class OrderDBModel(OrderUpdateModel, BaseOIDModel, metaclass=MongoMeta):
    stages: list[OrderStageModel] | None = None
    created_at: datetime | None = None
    # typing conflict with base classes
    client: ClientDBModel | None = None  # type: ignore[assignment]
    company_logistician: SotransUserDBModel | None = None
    subsidiary_id: PydanticObjectId = None
    carrier: OrganizationDBModel | None = None
    driver: DriverDBModel | None = None
    truck: TruckDBModel | None = None
    trailer: TrailerDBModel | None = None
    documents: list[DocumentDBModel] | None = None
    your_bid: BidDBModel | None = None
    best_bid: BidDBModel | None = None
    confirmation_end_time: datetime | None = None
    reservation_end_time: datetime | None = None
    deleted_at: datetime | None = None


class ResourceCheckOrderDBModel(OrderDBModel, metaclass=MongoMeta):
    resource_check_passing: bool | None = None


class ExchangeOrderUpdateModel(OrderUpdateModel):
    pass


class ConfirmedOrderUpdateModel(OrderUpdateModel):
    pass


class ActiveOrderUpdateModel(OrderUpdateModel):
    pass
