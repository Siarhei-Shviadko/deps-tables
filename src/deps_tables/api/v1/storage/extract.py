from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from deps_tables.api.models.image import ImageModel
from deps_tables.api.models.table import TableModel
from deps_tables.api.v1.storage.storage_downloader import get_file_from_storage
from deps_tables.application import ApplicationService
from deps_tables.containers import Application
from deps_tables.domain.constants import DEFAULT_LANGUAGE, DEFAULT_OCR_ENGINE

router = APIRouter()


@router.post(
    "/extract",
    response_model=TableModel,
)
@inject
def extract_tables_from_file_storage(
    image: ImageModel = Depends(get_file_from_storage),
    application: ApplicationService = Depends(Provide[Application.application]),
    ocr_engine: str = Body(DEFAULT_OCR_ENGINE, alias="ocrEngine"),
    language: str = Body(DEFAULT_LANGUAGE),
    table: TableModel = Body(...),
):
    result = application.ocr_tables(
        image=image.to_domain(),
        ocr_engine=ocr_engine,
        language=language,
        tables=[table.to_domain()],
    )
    if result:
        return asdict(result[0])

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "No data has been extracted"})
