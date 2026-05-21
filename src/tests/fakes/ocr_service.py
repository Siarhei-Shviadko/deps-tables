from collections import defaultdict
from typing import Dict, List, Optional

from deps_tables.domain.constants import DEFAULT_LANGUAGE
from deps_tables.domain.entities import ImageEntity, RectangleEntity, TextLineEntity
from deps_tables.infrastructure.services import OCRService


class FakeOCRService:
    def __init__(self):
        self._image_to_textline_dict: Dict[str, List[TextLineEntity]] = defaultdict(list)

    def add_textlines(self, image_path: str, textlines: List[TextLineEntity]):
        self._image_to_textline_dict[image_path].extend(textlines)

    def add_textline(self, image_path: str, textline: TextLineEntity):
        self._image_to_textline_dict[image_path].append(textline)

    def extract_data(
        self,
        image_obj: ImageEntity,
        engine: str,
        language: str = DEFAULT_LANGUAGE,
        bbox: Optional[RectangleEntity] = None,
    ) -> List[TextLineEntity]:
        textlines = []
        for textline in self._image_to_textline_dict[image_obj.blob_path]:
            for wordbox in textline.word_boxes:
                if wordbox.bbox.intersects_with(bbox):
                    textlines.append(textline)
                    break

        min_x = min([word_bbox.bbox.left_top_point.x for text_line in textlines for word_bbox in text_line.word_boxes])
        min_y = min([word_bbox.bbox.left_top_point.y for text_line in textlines for word_bbox in text_line.word_boxes])

        for text_line in textlines:
            # OCR returns coordinates in relation to extracted area, not all image
            # that's why shifting is required
            for word_bbox in text_line.word_boxes:
                word_bbox.bbox.left_top_point.x -= min_x
                word_bbox.bbox.left_top_point.y -= min_y
                word_bbox.bbox.right_bottom_point.x -= min_x
                word_bbox.bbox.right_bottom_point.y -= min_y
        return textlines
