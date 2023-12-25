from mongo_path.meta import MongoMeta
from pydantic import BaseModel, AnyUrl, AnyHttpUrl

from sotrans_models.models._base import BaseOIDModel
from sotrans_models.utils.make_partial_model import optional_fields_model


class CreateAdvertisingBlockModel(BaseModel):
    title: str
    target_url: str
    image_url: str


@optional_fields_model
class UpdateAdvertisingBlockModel(CreateAdvertisingBlockModel):
    is_active: bool | None = None


class AdvertisingBlockDBModel(BaseOIDModel, UpdateAdvertisingBlockModel, metaclass=MongoMeta):
    pass
