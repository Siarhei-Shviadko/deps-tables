import json
from typing import List

import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, File, UploadFile

from deps_tables.api.models.table import TableModel
from deps_tables.application import ApplicationService
from deps_tables.containers import Application
from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.domain.entities import ImageEntity, ImageMetadataEntity
from deps_tables.extras.ocr import TextLineModel

router = APIRouter()


def get_ocr_textlines(ocr_textlines: str = Body(..., alias="ocrTextlines")) -> List[TextLineModel]:
    return [TextLineModel(**textline) for textline in json.loads(ocr_textlines)]


@router.post("/extract-from-textlines", response_model=List[TableModel])
@inject
def extract_tables_from_image_and_textlines(
    file: UploadFile = File(...),
    ocr_textlines: List[TextLineModel] = Depends(get_ocr_textlines),
    source_id: str = Body("undefined", alias="sourceId"),
    application: ApplicationService = Depends(Provide[Application.application]),
):
    np_array = np.frombuffer(file.file.read(), dtype=np.uint8)
    cv2_image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
    image = ImageEntity(image=cv2_image)
    image.meta = ImageMetadataEntity(text_line_models=ocr_textlines, source_id=source_id)

    return application.detect_tables(
        image=image,
        table_detection_engine=TableDetectionEngineEnum.DEPS_CONVERTER,
        ocr_engine="",
        language="",
    )
