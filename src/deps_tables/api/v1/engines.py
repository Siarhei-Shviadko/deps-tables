from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from deps_tables.api.constants import DETECTION_ENGINE_NAMES, FREE_DETECTION_ENGINES
from deps_tables.api.models.table_detection_engine import TableDetectionEngineModel
from deps_tables.auth import get_current_user_organisation
from deps_tables.containers import Services
from deps_tables.domain.constants import TableDetectionEngineEnum

router = APIRouter(prefix="")


@router.get("/detection-engines", response_model=List[TableDetectionEngineModel])
@inject
def get_available_detection_engines(
    engines: List[TableDetectionEngineEnum] = Depends(Provide[Services.config.enabled_detectors]),
    restriction_enabled: bool = Depends(Provide[Services.config.paid_engines_restriction_enabled]),
    privileged_group: str = Depends(Provide[Services.config.privileged_group]),
):
    current_user_organisation = get_current_user_organisation()

    if restriction_enabled and current_user_organisation != privileged_group:
        engines = [e for e in engines if e in FREE_DETECTION_ENGINES]

    return [TableDetectionEngineModel(code=engine, name=DETECTION_ENGINE_NAMES[engine]) for engine in engines]
