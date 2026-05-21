import io
from typing import List, Optional

import cv2

from deps_tables.domain.constants import DEFAULT_LANGUAGE
from deps_tables.domain.entities import ImageEntity, RectangleEntity, TextLineEntity
from deps_tables.domain.interfaces import IOCRService
from deps_tables.extras.ocr import TextLine
from deps_tables.extras.ocr.exceptions import OCRError
from deps_tables.extras.services import OCRControllerService
from deps_tables.settings import Settings


class OCRService(IOCRService):
    def __init__(self, ocr_settings: Settings, ocr_service: OCRControllerService):
        self._settings = ocr_settings
        self._ocr_service = ocr_service

    def extract_data(
        self,
        image_obj: ImageEntity,
        engine: str,
        language: str = DEFAULT_LANGUAGE,
        bbox: Optional[RectangleEntity] = None,
    ) -> List[TextLineEntity]:
        """
        Extract text from image.
        If image was created from vector pdf, extracted data will be returned without OCR.
        :param image_obj:
        :param engine:
        :param language:
        :param bbox:
        :return:
        """

        image = image_obj.image
        if bbox is not None:
            width = bbox.right_bottom_point.x - bbox.left_top_point.x
            height = bbox.right_bottom_point.y - bbox.left_top_point.y
            if width <= 0 or height <= 0:
                return []

            image = image_obj.image[
                bbox.left_top_point.y : bbox.right_bottom_point.y,  # noqa: E203
                bbox.left_top_point.x : bbox.right_bottom_point.x,  # noqa: E203
            ]

        try:
            _, buffer = cv2.imencode(".png", image)
            ocr_response: List[TextLine] = self._ocr_service.extract_text(
                io.BytesIO(buffer.tobytes()),
                ocr_engine=engine,
                language=language,
            )
            return [TextLineEntity.from_domain(text_line) for text_line in ocr_response]
        except OCRError:
            return []

    def _extract_area_from_vector(
        self,
        text_data: List[TextLineEntity],
        bbox: Optional[RectangleEntity] = None,
    ) -> List[TextLineEntity]:
        if bbox is None:
            return text_data

        touched_word_boxes = []
        for textline in text_data:
            for word_box in textline.word_boxes:
                if word_box.bbox.intersects_with(bbox):
                    touched_word_boxes.append(word_box)

        return [
            TextLineEntity(
                id=1,
                word_boxes=touched_word_boxes,
            ),
        ]
