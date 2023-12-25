from enum import Enum

from sotrans_models.models.sections import Section
from sotrans_fastapi_keycloak.role import Role


class SotransRole(str, Enum):
    carrier_logistician: str = "carrier_logistician"
    carrier_director: str = "carrier_director"
    company_logistician: str = "company_logistician"
    company_manager: str = "company_manager"
    company_director: str = "company_director"
    admin: str = "admin"
    scraper: str = "scraper"
    inn_service: str = "inn_service"
    bid_service: str = "bid_service"
    notifications_worker: str = "notifications_worker"
    security_service: str = "security_service"
    cleanup_service: str = "cleanup_service"


sotrans_roles: dict[str, Role] = {}
sotrans_roles[SotransRole.carrier_logistician] = Role(
    allowed_sections=[
        Section.carriages_active,
        Section.carriages_assignment,
        Section.carriages_completed,
        Section.carriages_confirmed,
        Section.organization_profile,
        Section.organization_employees,
        Section.organization_docs,
        Section.resources_drivers,
        Section.resources_trailers,
        Section.resources_vehicles,
        Section.home,
        Section.user_profile,
        Section.user_notifications,
        Section.exchange,
    ]
)
sotrans_roles[SotransRole.carrier_director] = Role(
    ancestors=[sotrans_roles[SotransRole.carrier_logistician]],
)

sotrans_roles[SotransRole.company_logistician] = Role(
    ancestors=[sotrans_roles[SotransRole.carrier_logistician]],
    allowed_sections=[
        Section.carriages_active,
        Section.carriages_assignment,
        Section.carriages_completed,
        Section.carriages_confirmed,
        Section.organization_profile,
        Section.organization_employees,
        Section.organization_docs,
        Section.carriers,
        Section.resources_drivers,
        Section.resources_trailers,
        Section.resources_vehicles,
        Section.home,
        Section.user_profile,
        Section.user_notifications,
        Section.exchange,
    ],
)
sotrans_roles[SotransRole.company_manager] = Role(
    ancestors=[sotrans_roles[SotransRole.company_logistician]],
    allowed_sections=[Section.agents, Section.carriages_buffer],
)
sotrans_roles[SotransRole.company_director] = Role(
    ancestors=[
        sotrans_roles[SotransRole.company_manager],
        sotrans_roles[SotransRole.carrier_director],
    ],
)

sotrans_roles[SotransRole.admin] = Role(
    ancestors=[sotrans_roles[SotransRole.company_director]],
    allowed_sections=[Section.api],
)

sotrans_roles[SotransRole.inn_service] = Role(
    ancestors=[], allowed_sections=[],
)

sotrans_roles[SotransRole.notifications_worker] = Role(
    ancestors=[],
    allowed_sections=[Section.user_notifications],
)

sotrans_roles[SotransRole.bid_service] = Role(
    ancestors=[], allowed_sections=[]
)

sotrans_roles[SotransRole.scraper] = Role(
    ancestors=[], allowed_sections=[]
)

sotrans_roles[SotransRole.security_service] = Role(
    ancestors=[], allowed_sections=[]
)

sotrans_roles[SotransRole.cleanup_service] = Role(
    ancestors=[], allowed_sections=[]
)
