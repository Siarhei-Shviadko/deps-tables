from copy import deepcopy
from typing import List, Optional

from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.domain.entities import (
    AbsoluteAreaEntity,
    ImageEntity,
    RelativeAreaEntity,
    TableEntity,
)
from deps_tables.domain.entities.geom import Shift
from deps_tables.domain.services.ocr_table_service import OCRTableService
from deps_tables.domain.services.table_extraction_service import TableExtractionService
from deps_tables.extras.ocr import Point, Rectangle, TextLine, WordBox


class ApplicationService:
    def __init__(
        self,
        table_extraction_service: TableExtractionService,
        ocr_table_service: OCRTableService,
    ):
        self._table_extraction_service = table_extraction_service
        self._ocr_table_service = ocr_table_service

    def ocr_tables(
        self,
        image: ImageEntity,
        ocr_engine: str,
        language: str,
        tables: List[TableEntity],
    ) -> List[TableEntity]:
        extracted_tables = []
        for table in tables:
            extracted_tables.append(
                self._ocr_table_service.extract_data_from_table(image, table, engine=ocr_engine, language=language),
            )
        return extracted_tables

    def detect_tables(
        self,
        image: ImageEntity,
        table_detection_engine: TableDetectionEngineEnum,
        ocr_engine: str,
        language: str,
        selected_area: Optional[AbsoluteAreaEntity] = None,
    ) -> List[TableEntity]:
        global_shape = image.shape
        if selected_area is not None:
            image = self._get_subimage(image, selected_area)

        tables = self._table_extraction_service.execute(
            image=image,
            detector=table_detection_engine,
            ocr_engine=ocr_engine,
            language=language,
        )

        if selected_area is not None:
            relative_selected_area = RelativeAreaEntity.from_absolute(selected_area, global_shape)
            for table in tables:
                table.coordinates = table.coordinates.to_global(outer=relative_selected_area)

        return tables

    def _get_subimage(
        self,
        image_obj: ImageEntity,
        area: AbsoluteAreaEntity,
    ) -> ImageEntity:
        subimage = image_obj.image[area.top : area.bottom, area.left : area.right]

        meta = deepcopy(image_obj.meta)
        if meta and meta.textlines:
            meta.textlines = self._shift_textlines(image_obj.meta.textlines, area.shift)

        return ImageEntity(image=subimage, blob_path=None, meta=meta)

    def _shift_textlines(self, textlines: List[TextLine], shift: Shift[int]) -> List[TextLine]:
        return [
            TextLine(
                id=textline.id,
                word_boxes=[
                    WordBox(
                        content=word_box.content,
                        bbox=self._shift_rectangle(word_box.bbox, shift),
                        confidence=word_box.confidence,
                    )
                    for word_box in textline.word_boxes
                ],
            )
            for textline in textlines
        ]

    def _shift_rectangle(self, rect: Rectangle, shift: Shift[int]) -> Rectangle:
        return Rectangle(
            left_top_point=Point(
                x=rect.left_top_point.x - shift.x,
                y=rect.left_top_point.y - shift.y,
            ),
            right_bottom_point=Point(
                x=rect.right_bottom_point.x - shift.x,
                y=rect.right_bottom_point.y - shift.y,
            ),
        )
