from typing import List, Optional

from deps_tables.domain.constants import DEFAULT_LANGUAGE
from deps_tables.domain.entities import (
    ImageEntity,
    PointEntity,
    RectangleEntity,
    TextLineEntity,
    WordBoxEntity,
)
from deps_tables.domain.entities.geom import Shape
from deps_tables.domain.interfaces import IOCRService
from deps_tables.extras.ocr import BboxModel, OCRV3ResultModel, TextLineModel


class OCRDataConverter(IOCRService):
    """
    Convert existing TextLineModels to TextLineEntities either all data or with selection from current bbox
    """

    def extract_data(
        self,
        image_obj: ImageEntity,
        engine: str,
        language: Optional[str] = DEFAULT_LANGUAGE,
        bbox: Optional[RectangleEntity] = None,
    ) -> List[TextLineEntity]:
        ocr_data = image_obj.meta.text_line_models if image_obj.meta and image_obj.meta.text_line_models else None
        if bbox and ocr_data:
            return self._choose_from_ocr_data(bbox, ocr_data, image_obj.shape)
        if ocr_data:
            return [self._convert_text_line_model_to_domain(data, image_obj.shape) for data in ocr_data]
        return []

    def _choose_from_ocr_data(
        self,
        bbox: RectangleEntity,
        ocr_data: List[TextLineModel],
        image_shape: Shape,
    ) -> List[TextLineEntity]:
        v3_ocr_data = OCRV3ResultModel(textlines=ocr_data)
        table_bbox = self._convert_rectangle_entity_to_bbox_model(bbox, image_shape)
        lines = []
        for line in ocr_data:
            ocr_wboxes = []
            for ocr_wbox in line.word_boxes:
                if v3_ocr_data.is_intersected_by_box(table_bbox, ocr_wbox.bbox):
                    ocr_wboxes.append(ocr_wbox)
            if ocr_wboxes:
                lines.append(TextLineModel(id=line.id, word_boxes=ocr_wboxes))
                ocr_wboxes.clear()
        return [self._convert_text_line_model_to_domain(data, image_shape) for data in lines]

    @staticmethod
    def _convert_rectangle_entity_to_bbox_model(bbox: RectangleEntity, image_shape: Shape) -> BboxModel:
        y = bbox.left_top_point.y / image_shape.height
        x = bbox.left_top_point.x / image_shape.width
        return BboxModel(
            y=y,
            x=x,
            w=(bbox.right_bottom_point.x / image_shape.width) - x,
            h=(bbox.right_bottom_point.y / image_shape.height) - y,
            page=1,
        )

    @staticmethod
    def _convert_text_line_model_to_domain(model: TextLineModel, image_shape: Shape) -> TextLineEntity:
        return TextLineEntity(
            id=model.id,
            word_boxes=[
                WordBoxEntity(
                    content=word_box.content,
                    bbox=RectangleEntity(
                        left_top_point=PointEntity(
                            x=int(word_box.bbox.left * image_shape.width),
                            y=int(word_box.bbox.top * image_shape.height),
                        ),
                        right_bottom_point=PointEntity(
                            x=int(word_box.bbox.right * image_shape.width),
                            y=int(word_box.bbox.bottom * image_shape.height),
                        ),
                    ),
                    confidence=word_box.confidence,
                )
                for word_box in model.word_boxes
            ],
        )
