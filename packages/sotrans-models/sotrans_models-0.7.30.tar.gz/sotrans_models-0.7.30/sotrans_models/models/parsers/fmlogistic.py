from pydantic import BaseModel
from typing import Optional


class FmlogisticOrderModel(BaseModel):
    id: Optional[str] = None
    shippingNumber: Optional[str] = None
    vehicleType: Optional[str] = None
    weightKg: Optional[float] = None
    basicDeliveryCostWithoutVAT: Optional[float] = None
    additionalCostsWithoutVAT: Optional[float] = None
    totalDeliveryCost: Optional[float] = None
    status: Optional[str] = None
    isDeleted: bool
    initialStatus: Optional[str] = None
    firstLoadingCity: Optional[str] = None
    firstLoadingAddress2And3: Optional[str] = None
    firstLoadingDateTime: Optional[str] = None
    lastUnloadingAddress2And3: Optional[str] = None
    lastUnloadingCity: Optional[str] = None
    lastUnloadingDateTime: Optional[str] = None
    loadingStoppersCount: Optional[int] = None
    unloadingStoppersCount: Optional[int] = None
    shippingCargoUnits: Optional[str] = None
    fromWhere: Optional[str] = None
    whereTo: Optional[str] = None
    paymentTermDays: Optional[str] = None
    totalDeliveryCostWithDiscount: Optional[float] = None
    totalDeliveryCostWithDiscountVAT: Optional[float] = None
    statusChangedAt: str
    isChanged: bool
    lastCheckedTime: str
    lastChangedTime: str
    link: str
