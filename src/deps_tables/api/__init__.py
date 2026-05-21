from fastapi import APIRouter

from .debug import router as debug_router
from .healthcheck import healthcheck_router
from .service_info import service_info_router
from .v1 import router as v1_router

router = APIRouter()

router.include_router(v1_router, prefix="/v1")
router.include_router(debug_router)
router.include_router(service_info_router)
router.include_router(healthcheck_router)
