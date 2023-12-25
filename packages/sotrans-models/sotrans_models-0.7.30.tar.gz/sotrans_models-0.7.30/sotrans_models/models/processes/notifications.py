from enum import Enum


class NotificationDataTypes(str, Enum):
    TENDER_INVITE = "tender_invite"
    TENDER_OPEN = "tender_open"
    TRANSPORTATION_LOADING_ARRIVAL = "transportation_loading_arrival"
    TRANSPORTATION_LOADING_DEPARTURE = "transportation_loading_departure"
    TRANSPORTATION_UNLOADING_ARRIVAL = "transportation_unloading_arrival"
    TRANSPORTATION_UNLOADING_DEPARTURE = "transportation_unloading_departure"
    START_ORDER = "start_order"
    CANCEL_TRANSPORTATION_BY_ORGANIZER = "cancel_transportation_by_organizer"
    CANCEL_TRANSPORTATION_BY_EXECUTOR = "cancel_transportation_by_executor"
    TRANSPORTATION_DISTRIBUTION = "transportation_distribution"
    TRANSPORTATION_DISTRIBUTION_BY_QUOTAS = "transportation_distribution_by_quotas"
    TRANSPORTATION_DISTRIBUTION_BY_RATES = "transportation_distribution_by_rates"
    BID_EVENT = "bid_event"
    ORDER_TAKEN = "order_taken"
