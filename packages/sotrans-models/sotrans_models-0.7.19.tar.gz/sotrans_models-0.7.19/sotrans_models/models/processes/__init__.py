from enum import Enum


class Processes(str, Enum):
    company_verification = "sotrans.Organizations.companyVerification"
    bid_tracking = "sotrans.Bids.trackBids"
