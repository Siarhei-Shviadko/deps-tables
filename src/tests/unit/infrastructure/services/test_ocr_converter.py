import pytest
from mock import Mock

from deps_tables.domain.entities.geom import Shape
from tests.data import full_converted_result, text_line_models


@pytest.fixture
def image_obj_mock():
    mock = Mock()
    mock.shape = Shape(width=2550, height=3300)
    mock.meta.text_line_models = text_line_models
    return mock


class TestOCRV3Service:
    def test_extract_data__empty_ocr_data__empty_list(self, ocr_converter, image_obj_mock):
        image_obj_mock.meta.text_line_models = []
        res = ocr_converter.extract_data(
            image_obj=image_obj_mock,
            engine="engine",
        )

        assert res == []

    def test_extract_data__ocr_data__full_converted_data(self, ocr_converter, image_obj_mock):
        res = ocr_converter.extract_data(
            image_obj=image_obj_mock,
            engine="engine",
        )

        assert res == full_converted_result

    def test_extract_data__ocr_data__bbox__chosen_one_bbox(self, ocr_converter, image_obj_mock):
        bbox = full_converted_result[0].word_boxes[0].bbox
        res = ocr_converter.extract_data(
            image_obj=image_obj_mock,
            engine="engine",
            bbox=bbox,
        )
        expected = [full_converted_result[0]]
        expected[0].word_boxes = [expected[0].word_boxes[0]]

        assert res == expected

    def test_extract_data__ocr_data__not_existing_bbox__empty_list(self, ocr_converter, image_obj_mock):
        bbox = full_converted_result[0].word_boxes[0].bbox
        bbox.left_top_point.x = bbox.left_top_point.y = 0
        bbox.right_bottom_point.x = bbox.right_bottom_point.y = 1
        res = ocr_converter.extract_data(
            image_obj=image_obj_mock,
            engine="engine",
            bbox=bbox,
        )

        assert res == []

    def test_extract_data__bbox__empty_list(self, ocr_converter, image_obj_mock):
        image_obj_mock.meta.text_line_models = []
        bbox = full_converted_result[0].word_boxes[0].bbox
        res = ocr_converter.extract_data(
            image_obj=image_obj_mock,
            engine="engine",
            bbox=bbox,
        )

        assert res == []
