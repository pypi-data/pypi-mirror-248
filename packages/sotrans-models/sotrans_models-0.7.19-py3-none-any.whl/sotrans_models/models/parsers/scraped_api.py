from pydantic import BaseModel

from sotrans_models.models._base import BaseIdModel
from sotrans_models.models._mongo import PydanticObjectId
from sotrans_models.models.orders.order import OrderDBModel, OrderUpdateModel


class ScrapedOrdersDataModel(BaseIdModel):
    scraped: list[OrderDBModel]


class ScrapedOrdersUpdatesModels(BaseIdModel):
    scraped_updates: list[OrderUpdateModel]


class ScrapedOrdersOIDsResponse(BaseIdModel):
    scraped_ids: list[PydanticObjectId]


class UpdatedScrapedOrderUrl(BaseModel):
    scraped_urls: list[str]
