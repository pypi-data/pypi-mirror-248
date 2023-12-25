from enum import Enum

from pydantic import BaseModel, Field
from sotrans_fastapi_keycloak._uuid import PydanticUUID

from sotrans_models.models._mongo import PydanticObjectId


class PublishMessageOnBids(str, Enum):
    # correlated by order_id
    clients_price = "sotrans.BidTracker.ContractorsPrice"
    carrier_assigned_by_logistician = "sotrans.BidTracker.ThroughAuction"
    stop_auction = "sotrans.BidTracker.AuctionFinished"

    # correlation key - bid_id
    bid_out = "sotrans.BidTracker.OutBid"
    bid_removed_by_requester = "sotrans.BidTracker.BidRemoval"


class ExtraBidTrackingVars(BaseModel):
    id: str | int
    date: str
    departure_date: str = Field(serialization_alias='departureDate')
    route: dict


class ExtraType(str, Enum):
    order = "order"
    general = "general"


class BidTrackingVariables(BaseModel):
    order_id: PydanticObjectId
    bid_id: PydanticObjectId
    duration: str
    user_id: PydanticUUID
    extra_type: ExtraType = ExtraType.order
    extra: ExtraBidTrackingVars = Field(default_factory=dict)


class PrevBidOwnerModel(BaseModel):
    bid_id: PydanticObjectId | None = None
    user_id: PydanticUUID | None = None
