from datetime import datetime

from mongo_path.meta import MongoMeta

from sotrans_models.models._base import BaseOIDModel, InsertByOIDModel
from sotrans_models.models._mongo import PydanticObjectId
from sotrans_models.models.users import SotransUserDBModel
from sotrans_models.models.organizations import OrganizationDBModel
from pydantic import BaseModel

from sotrans_models.utils.make_partial_model import optional_fields_model


class BidCreateModel(BaseModel):
    value: int
    order_id: PydanticObjectId


@optional_fields_model
class BidOptionalsModel(BidCreateModel):
    pass


class BidDBModel(BidOptionalsModel, BaseOIDModel, metaclass=MongoMeta):
    client_id: PydanticObjectId = None
    owner: SotransUserDBModel | None = None
    created_at: datetime | None = None
    carrier: OrganizationDBModel | None = None


class EndAuctionRequestModel(BaseModel):
    carrier: InsertByOIDModel | None = None
