from dataclasses import asdict
from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends

from deps_tables.api.models.coordinates import RelativeAreaModelWithPage
from deps_tables.api.models.image import ImageModel
from deps_tables.api.models.table import TableModel
from deps_tables.api.v1.storage.storage_downloader import get_file_from_storage
from deps_tables.application import ApplicationService
from deps_tables.containers import Application
from deps_tables.domain.constants import (
    DEFAULT_LANGUAGE,
    DEFAULT_OCR_ENGINE,
    DEFAULT_TABLE_DETECTOR,
    TableDetectionEngineEnum,
)
from deps_tables.domain.entities import (
    ImageEntity,
    ImageMetadataEntity,
    RelativeAreaEntityWithPage,
)
from deps_tables.infrastructure.access_management.table_detection_engine_accessor import (
    check_user_has_permission_to_engine,
)

router = APIRouter()


def add_source_id_to_meta(image: ImageEntity, source_id: Optional[str]):
    image.meta = image.meta or ImageMetadataEntity()
    image.meta.source_id = source_id


@router.post(
    "/detect",
    response_model=List[TableModel],
)
@inject
def detect_extract_tables_from_file_storage(
    image: ImageModel = Depends(get_file_from_storage),
    application: ApplicationService = Depends(Provide[Application.application]),
    ocr_engine: str = Body(DEFAULT_OCR_ENGINE, alias="ocrEngine"),
    table_detection_engine: TableDetectionEngineEnum = Body(DEFAULT_TABLE_DETECTOR, alias="tableDetectionEngine"),
    language: str = Body(DEFAULT_LANGUAGE),
    area: Optional[RelativeAreaModelWithPage] = Body(None),
    source_id: str = Body(None, alias="sourceId"),
):
    check_user_has_permission_to_engine(table_detection_engine)

    image_entity = image.to_domain()
    add_source_id_to_meta(image_entity, source_id)
    detected_tables = application.detect_tables(
        image=image_entity,
        table_detection_engine=table_detection_engine,
        language=language,
        ocr_engine=ocr_engine,
        selected_area=RelativeAreaEntityWithPage(**area.dict()).to_absolute(image.shape) if area is not None else None,
    )
    return [asdict(table) for table in detected_tables]
