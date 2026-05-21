from copy import deepcopy

import cv2
import numpy as np
import pytest

from deps_tables.domain.entities import ImageEntity
from tests.data.tables_data import (
    tables_with_bbox_entities,
    textlines_for_table_with_bboxes,
)
from tests.fakes.ocr_service import FakeOCRService


@pytest.fixture
def ocr_service(application):
    with application.core.ocr_service.override(FakeOCRService()) as ocr_service:
        yield ocr_service()


@pytest.fixture
def ocr_table_service(application, ocr_service):
    application.reset_singletons()
    yield application.core.ocr_table()


@pytest.fixture
def bbox_table():
    return tables_with_bbox_entities[0]


@pytest.fixture
def textlines_for_bbox_table():
    return textlines_for_table_with_bboxes


@pytest.fixture
def empty_bbox_table(bbox_table):
    result = deepcopy(bbox_table)
    for cell in result.cells:
        cell.value = None
    return result


@pytest.fixture
def image():
    with open("tests/data/table.png", "rb") as f:
        np_array = np.frombuffer(f.read(), dtype=np.uint8)
    cv2_image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
    return ImageEntity(blob_path="a/b/table.png", image=cv2_image)
