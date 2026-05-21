import cv2
import numpy as np
import pytest

import deps_tables.infrastructure.heuristic.utils as util
from deps_tables.containers import Application
from deps_tables.domain.entities import BoundingBoxEntity
from deps_tables.infrastructure.heuristic.columns_detection import ColumnsCorrection
from deps_tables.infrastructure.heuristic.rows_detection import RowsIdentifier
from deps_tables.infrastructure.table_extractors.deps_table_extractor import (
    DepsTablesExtractor,
)


def test_column_identifier_with_table(column_identifier):
    image_path = "tests/data/image_with_table.jpg"
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    boxes = column_identifier.identify_borders(img)

    assert len(boxes) == 7
    assert type(boxes[0]) == BoundingBoxEntity


def test_cell_identifier(cell_identifier):
    image_path = "tests/data/image_with_cells.jpg"
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    boxes = cell_identifier.identify_borders(img)

    assert len(boxes) == 23
    assert type(boxes[0]) == BoundingBoxEntity


def test_checking_table_existence__with_table(table_identifier_service):
    image_path = "tests/data/image_with_table.jpg"

    with open(image_path, "rb") as f:
        np_array = np.frombuffer(f.read(), dtype=np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)

    table_exist = table_identifier_service.is_table_on_page(image)
    assert table_exist is True


@pytest.mark.skip
def test_checking_table_existence__without_table(table_identifier_service):
    image_path = "tests/data/image_without_table.jpg"

    with open(image_path, "rb") as f:
        np_array = np.frombuffer(f.read(), dtype=np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)

    table_exist = table_identifier_service.is_table_on_page(image)
    assert table_exist is False
