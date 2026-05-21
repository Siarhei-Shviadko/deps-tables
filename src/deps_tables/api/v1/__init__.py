from fastapi import APIRouter

from .engines import router as engines_router
from .file import router as file_router
from .storage import router as storage_router

router = APIRouter()

router.include_router(storage_router)
router.include_router(file_router)
router.include_router(engines_router, tags=["Table Detection Engines"])
