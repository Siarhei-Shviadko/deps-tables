import cv2
import numpy as np

from deps_tables.domain.entities import ImageEntity


def test_extract_tables__no_ocr__return_tables(deps_table_extractor, mocker) -> None:
    deps_table_extractor._ocr_service.extract_data = mocker.Mock(return_value=[])
    image_path = "tests/data/test_tables.jpg"
    with open(image_path, "rb") as fp:
        np_array = np.frombuffer(fp.read(), dtype=np.uint8)

    image = ImageEntity(
        image=cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE),
        blob_path="some_name",
    )

    tables = deps_table_extractor.extract_tables(
        image_obj=image,
        ocr_engine="TESSERACT",
        language="eng",
    )

    assert len(tables) == 3

    shapes = [(len(table.rows), len(table.columns)) for table in tables]
    assert (5, 4) in shapes
    assert (14, 4) in shapes
    assert (11, 4) in shapes
