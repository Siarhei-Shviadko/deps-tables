from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from deps_tables.api.constants import FREE_DETECTION_ENGINES
from deps_tables.auth import get_current_user_organisation
from deps_tables.containers import Application
from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.domain.exceptions import ForbiddenError


@inject
def check_user_has_permission_to_engine(
    engine: TableDetectionEngineEnum,
    restriction_enabled: bool = Depends(Provide[Application.config.paid_engines_restriction_enabled]),
    privileged_group: str = Depends(Provide[Application.config.privileged_group]),
) -> None:
    current_user_organisation = get_current_user_organisation()
    if restriction_enabled and engine not in FREE_DETECTION_ENGINES and current_user_organisation != privileged_group:
        raise ForbiddenError(f"Engine ({engine}) is not free and current user has no permission for using it")
