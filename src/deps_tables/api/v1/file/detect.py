from dataclasses import asdict
from typing import List, Optional

import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, File, UploadFile

from deps_tables.api.models.table import TableModel
from deps_tables.application import ApplicationService
from deps_tables.containers import Application
from deps_tables.domain.constants import (
    DEFAULT_LANGUAGE,
    DEFAULT_OCR_ENGINE,
    DEFAULT_TABLE_DETECTOR,
    TableDetectionEngineEnum,
)
from deps_tables.domain.entities import ImageEntity, ImageMetadataEntity
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
def detect_extract_tables_from_file(
    file: UploadFile = File(...),
    application: ApplicationService = Depends(Provide[Application.application]),
    ocr_engine: str = Body(DEFAULT_OCR_ENGINE, alias="ocrEngine"),
    table_detection_engine: TableDetectionEngineEnum = Body(DEFAULT_TABLE_DETECTOR, alias="tableDetectionEngine"),
    language: str = Body(DEFAULT_LANGUAGE),
    source_id: str = Body(None, alias="sourceId"),
):
    check_user_has_permission_to_engine(table_detection_engine)

    np_array = np.frombuffer(file.file.read(), dtype=np.uint8)
    cv2_image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
    image = ImageEntity(image=cv2_image)
    add_source_id_to_meta(image, source_id)
    detected_tables = application.detect_tables(
        image=image,
        table_detection_engine=table_detection_engine,
        ocr_engine=ocr_engine,
        language=language,
    )
    return [asdict(table) for table in detected_tables]
