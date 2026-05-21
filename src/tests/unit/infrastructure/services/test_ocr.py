import io

import cv2
import mock
import numpy as np
import pytest

from deps_tables.domain.constants import DEFAULT_LANGUAGE
from deps_tables.domain.entities import (
    ImageEntity,
    ImageMetadataEntity,
    PointEntity,
    RectangleEntity,
    TextLineEntity,
    WordBoxEntity,
)
from deps_tables.extras.ocr.exceptions import OCRError


@pytest.fixture(scope="function")
def image():
    surface = np.zeros((100, 100), dtype=np.uint8)

    image = ImageEntity(
        image=surface,
        blob_path=None,
        meta=None,
    )

    return image


@pytest.fixture(scope="class")
def text_line():
    text_line = TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1, y=2),
                    right_bottom_point=PointEntity(x=11, y=12),
                ),
                content="Word",
            )
        ],
    )

    return text_line


class TestOCRService:
    def test_is_intersected__not_intersected_atall(self):
        rec1 = RectangleEntity(
            left_top_point=PointEntity(
                x=0,
                y=0,
            ),
            right_bottom_point=PointEntity(
                x=100,
                y=100,
            ),
        )
        rec2 = RectangleEntity(
            left_top_point=PointEntity(
                x=101,
                y=0,
            ),
            right_bottom_point=PointEntity(
                x=101,
                y=100,
            ),
        )
        assert rec1.intersects_with(rec2) == False
        assert rec2.intersects_with(rec1) == False

    def test_is_intersected__intersected_almost_full(self, ocr_service):
        rec1 = RectangleEntity(
            left_top_point=PointEntity(
                x=0,
                y=0,
            ),
            right_bottom_point=PointEntity(
                x=100,
                y=100,
            ),
        )
        rec2 = RectangleEntity(
            left_top_point=PointEntity(
                x=1,
                y=1,
            ),
            right_bottom_point=PointEntity(
                x=101,
                y=101,
            ),
        )

        assert rec1.intersects_with(rec2) == True
        assert rec2.intersects_with(rec1) == True

    def test_is_intersected__partialy_intersected_lower_threshold(self, ocr_service):
        rec1 = RectangleEntity(
            left_top_point=PointEntity(
                x=0,
                y=0,
            ),
            right_bottom_point=PointEntity(
                x=10,
                y=10,
            ),
        )
        rec2 = RectangleEntity(
            left_top_point=PointEntity(
                x=2,
                y=2,
            ),
            right_bottom_point=PointEntity(
                x=12,
                y=12,
            ),
        )

        assert rec1.intersects_with(rec2) == False
        assert rec2.intersects_with(rec1) == False

    def test_is_intersected__partialy_intersected_upper_threshold(self, ocr_service):
        rec1 = RectangleEntity(
            left_top_point=PointEntity(
                x=0,
                y=0,
            ),
            right_bottom_point=PointEntity(
                x=10,
                y=10,
            ),
        )
        rec2 = RectangleEntity(
            left_top_point=PointEntity(
                x=1,
                y=2,
            ),
            right_bottom_point=PointEntity(
                x=11,
                y=12,
            ),
        )

        assert rec1.intersects_with(rec2) == True
        assert rec2.intersects_with(rec1) == True

    def test_extract_data__image_without_bbox(self, ocr_service, image, text_line):
        ocr_service._ocr_service.extract_text.return_value = [text_line]

        actual = ocr_service.extract_data(
            image_obj=image,
            engine="TESSERACT",
        )
        expected = [text_line]
        assert actual == expected
        ocr_service._ocr_service.extract_text.assert_called_with(
            mock.ANY,
            ocr_engine="TESSERACT",
            language=DEFAULT_LANGUAGE,
        )

    def test_extract_data__ocr_error__empty_list(self, ocr_service, image):
        ocr_service._ocr_service.extract_text.side_effect = OCRError

        res = ocr_service.extract_data(
            image_obj=image,
            engine="TESSERACT",
        )

        assert res == []

    def test_extract_data__image_with_bbox(self, ocr_service, image, text_line):
        ocr_service._ocr_service.extract_text.return_value = [text_line]

        actual = ocr_service.extract_data(
            image_obj=image,
            engine="TESSERACT",
            bbox=RectangleEntity(
                left_top_point=PointEntity(x=25, y=25),
                right_bottom_point=PointEntity(x=75, y=75),
            ),
        )
        expected = [text_line]
        assert actual == expected
        ocr_service._ocr_service.extract_text.assert_called_with(
            mock.ANY,
            ocr_engine="TESSERACT",
            language=DEFAULT_LANGUAGE,
        )

    @pytest.mark.skip
    def test_extract_data__image_with_valid_vector_cache__return_result(self, ocr_service, image):
        textlines = [
            TextLineEntity(
                id=1,
                word_boxes=[
                    WordBoxEntity(
                        bbox=RectangleEntity(
                            left_top_point=PointEntity(x=0, y=0),
                            right_bottom_point=PointEntity(x=50, y=10),
                        ),
                        content="A",
                    ),
                    WordBoxEntity(
                        bbox=RectangleEntity(
                            left_top_point=PointEntity(x=50, y=0),
                            right_bottom_point=PointEntity(x=100, y=10),
                        ),
                        content="B",
                    ),
                ],
            ),
            TextLineEntity(
                id=2,
                word_boxes=[
                    WordBoxEntity(
                        bbox=RectangleEntity(
                            left_top_point=PointEntity(x=0, y=10),
                            right_bottom_point=PointEntity(x=50, y=20),
                        ),
                        content="C",
                    ),
                    WordBoxEntity(
                        bbox=RectangleEntity(
                            left_top_point=PointEntity(x=50, y=10),
                            right_bottom_point=PointEntity(x=100, y=20),
                        ),
                        content="D",
                    ),
                ],
            ),
        ]
        image.meta = ImageMetadataEntity(
            textlines=textlines,
        )

        actual = ocr_service.extract_data(
            image_obj=image,
            engine="TESSERACT",
            bbox=RectangleEntity(
                left_top_point=PointEntity(x=50, y=0),
                right_bottom_point=PointEntity(x=85, y=20),
            ),
        )
        expected = [
            TextLineEntity(
                id=1,
                word_boxes=[
                    WordBoxEntity(
                        bbox=RectangleEntity(
                            left_top_point=PointEntity(x=50, y=0),
                            right_bottom_point=PointEntity(x=100, y=10),
                        ),
                        content="B",
                    ),
                    WordBoxEntity(
                        bbox=RectangleEntity(
                            left_top_point=PointEntity(x=50, y=10),
                            right_bottom_point=PointEntity(x=100, y=20),
                        ),
                        content="D",
                    ),
                ],
            )
        ]
        assert actual == expected
