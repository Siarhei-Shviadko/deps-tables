from fastapi import APIRouter

from .detect import router as detect_router
from .extract import router as extract_router

router = APIRouter(prefix="/storage", tags=["Storage"])

router.include_router(detect_router)
router.include_router(extract_router)
