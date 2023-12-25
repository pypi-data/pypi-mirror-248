from pydantic import BaseModel


class CountResponse(BaseModel):
    count: int


class OneMonthStatsModel(BaseModel):
    key: int
    value: int


class MonthlyStatisticsResponse(BaseModel):
    graph: list[OneMonthStatsModel]
    total: int


class ErrorRepr(BaseModel):
    detail: str


class ErrorMessage(BaseModel):
    message: str
