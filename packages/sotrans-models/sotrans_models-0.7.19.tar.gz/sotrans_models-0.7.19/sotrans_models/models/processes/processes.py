from mongo_path.meta import MongoMeta
from pydantic import BaseModel


class ProcessModel(BaseModel, metaclass=MongoMeta):
    pid: int
    zeebe_url: str
    variables: dict
