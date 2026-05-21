import statistics
from contextlib import suppress
from typing import List

from more_itertools import flatten

from deps_tables.domain.entities import (
    AbsoluteAreaEntity,
    ImageEntity,
    PointEntity,
    RectangleEntity,
    TableEntity,
    TextLineEntity,
)
from deps_tables.domain.entities.geom import Shape
from deps_tables.infrastructure.services import OCRService


class OCRTableService:
    def __init__(self, ocr_service: OCRService):
        self._ocr_service: OCRService = ocr_service

    def extract_data_from_table(self, image: ImageEntity, table: TableEntity, engine: str, language: str) -> TableEntity:
        table_coords = table.coordinates or table.source_bbox_coordinates.bboxes[0]
        table_absolute_coords = table_coords.to_absolute(image.shape)
        table_rectangle = self._build_absolute_area_rectangle(table_absolute_coords)
        table_data: List[TextLineEntity] = self._ocr_service.extract_data(
            image,
            engine,
            language,
            table_rectangle,
        )
        self._align_area_coords_to_document_coords(table_rectangle.left_top_point, table_data)
        self.process_old_format_data(image.shape, table, table_data)
        self._process_source_coordinates(image.shape, table, table_data)
        return table

    def process_old_format_data(self, shape: Shape[int], table: TableEntity, table_ocr: List[TextLineEntity]) -> None:
        if not self._old_format_processable(table):
            return
        for cell in table.cells:
            cell_area = table.calculate_cell_global_coords(cell.coordinates).to_absolute(shape)
            cell_rect = self._build_absolute_area_rectangle(cell_area)
            cell_data: List[TextLineEntity] = self.match_absolute_area(table_ocr, cell_rect)
            cell.value = self._merge_cell_data([cell_data])
            cell.confidence = self._calc_cell_confidence([cell_data])

    @staticmethod
    def _old_format_processable(table: TableEntity) -> bool:
        return all((table.coordinates, table.columns, table.rows))

    def _process_source_coordinates(self, shape: Shape[int], table: TableEntity, table_ocr: List[TextLineEntity]) -> None:
        if not table.source_bbox_coordinates:
            return
        for cell in table.cells:
            cell_datas = []
            for coordinate in cell.source_bbox_coordinates:
                for bbox in coordinate.bboxes:
                    rectangle = self._build_absolute_area_rectangle(bbox.to_absolute(shape))
                    cell_data: List[TextLineEntity] = self.match_absolute_area(table_ocr, rectangle)
                    cell_datas.append(cell_data)
            cell.value = self._merge_cell_data(cell_datas)
            cell.confidence = self._calc_cell_confidence(cell_datas)

    @staticmethod
    def _calc_cell_confidence(cell_data: List[List[TextLineEntity]]) -> float:
        with suppress(statistics.StatisticsError):
            return statistics.mean(word.confidence for textline in flatten(cell_data) for word in textline.word_boxes)
        return 1.0

    @staticmethod
    def _merge_cell_data(cell_data: List[List[TextLineEntity]]) -> str:
        return " ".join((word.content for text_line in flatten(cell_data) for word in text_line.word_boxes))

    @staticmethod
    def _build_absolute_area_rectangle(cell_area: AbsoluteAreaEntity) -> RectangleEntity:
        return RectangleEntity(
            left_top_point=PointEntity(
                x=cell_area.left,
                y=cell_area.top,
            ),
            right_bottom_point=PointEntity(
                x=cell_area.right,
                y=cell_area.bottom,
            ),
        )

    @staticmethod
    def match_absolute_area(table_ocr: List[TextLineEntity], cell_area: RectangleEntity) -> List[TextLineEntity]:
        idx = 0
        cell_ocr = []
        for line in table_ocr:
            curr_words = []
            for word in line.word_boxes:
                if word.bbox.is_inside(cell_area):
                    curr_words.append(word)
            if not curr_words:
                continue
            cell_ocr.append(TextLineEntity(id=idx, word_boxes=curr_words))
            idx += 1
        return cell_ocr

    @staticmethod
    def _align_area_coords_to_document_coords(
        extracted_table_left_top_point: PointEntity,
        ocr_table_data: List[TextLineEntity],
    ) -> None:
        def align_point_coords_with_document_coords(shifted_point: PointEntity, start_point: PointEntity) -> None:
            shifted_point.x += start_point.x
            shifted_point.y += start_point.y

        for text_line in ocr_table_data:
            for word_box in text_line.word_boxes:

                align_point_coords_with_document_coords(
                    word_box.bbox.left_top_point,
                    extracted_table_left_top_point,
                )
                align_point_coords_with_document_coords(
                    word_box.bbox.right_bottom_point,
                    extracted_table_left_top_point,
                )
