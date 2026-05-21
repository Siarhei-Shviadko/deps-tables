import logging
import time
from enum import Enum
from operator import attrgetter
from typing import List, Optional, Tuple

import cv2
from azure.ai.formrecognizer import (
    AnalyzeResult,
    BoundingRegion,
    DocumentAnalysisClient,
    DocumentTable,
    DocumentTableCell,
    DocumentWord,
)
from azure.core.credentials import AzureKeyCredential

from deps_tables.domain.constants import AZURE_OCR_ENGINE, DEFAULT_OCR_ENGINE
from deps_tables.domain.entities import (
    CellCoordinates,
    CellEntity,
    ColumnEntity,
    ImageEntity,
    RelativeAreaEntityWithPage,
    RowEntity,
    TableEntity,
)
from deps_tables.domain.entities.geom import Shape
from deps_tables.domain.interfaces import ITableAdapter, ITableExtractor
from deps_tables.domain.services import OCRTableService

_logger = logging.getLogger(__name__)


class AzureTableAdapter(ITableAdapter):
    @classmethod
    def convert_to_domain_table(cls, response: AnalyzeResult, source_id: Optional[str] = None) -> List[TableEntity]:
        words = response.pages[0].words + response.pages[0].selection_marks
        tables = []
        page = response.pages[0]
        shape = Shape(width=page.width, height=page.height)
        for table in response.tables:
            table_coordinates = cls.bounding_regions_to_area(table.bounding_regions, shape)
            new_table = TableEntity(
                coordinates=table_coordinates,
                columns=cls.create_table_columns(table, table_coordinates, shape),
                rows=cls.create_table_rows(table, table_coordinates, shape),
                cells=cls.create_table_cells(table, words),
            )
            if source_id:
                new_table.fill_source_bbox_coordinates(source_id)
            tables.append(new_table)

        tables.sort(key=lambda x: (x.coordinates.top, x.coordinates.left))

        return tables

    @classmethod
    def create_table_columns(
        cls,
        table: DocumentTable,
        table_coordinates: RelativeAreaEntityWithPage,
        shape: Shape[float],
    ) -> List[ColumnEntity]:
        col_coords = cls._get_axis_coordinates(table, "column", shape)
        return [
            ColumnEntity(x=max(0, x)) for x in cls.coords_to_relative(col_coords, table_coordinates.left, table_coordinates.width)
        ]

    @classmethod
    def create_table_rows(
        cls,
        table: DocumentTable,
        table_coordinates: RelativeAreaEntityWithPage,
        shape: Shape[float],
    ) -> List[RowEntity]:
        row_coords = cls._get_axis_coordinates(table, "row", shape)
        return [
            RowEntity(y=max(0, y)) for y in cls.coords_to_relative(row_coords, table_coordinates.top, table_coordinates.height)
        ]

    @classmethod
    def create_table_cells(cls, table: DocumentTable, words: List[DocumentWord]) -> List[CellEntity]:
        return [
            CellEntity(
                value=table_cell.content,
                coordinates=CellCoordinates(
                    column=table_cell.column_index,
                    row=table_cell.row_index,
                    column_span=table_cell.column_span,
                    row_span=table_cell.row_span,
                ),
                confidence=cls._calc_cell_confidence(table_cell, words),
            )
            for table_cell in table.cells
        ]

    @classmethod
    def _calc_cell_confidence(cls, cell: DocumentTableCell, words: List[DocumentWord]) -> float:
        def is_word_in_cell(word) -> bool:
            return any(span.offset <= word.span.offset < span.offset + span.length for span in cell.spans)

        if not cell.spans:
            return 1.0
        cell_words = list(filter(is_word_in_cell, words))
        if not cell_words:
            return 1.0
        return min(map(attrgetter("confidence"), cell_words))

    @classmethod
    def _cell_to_idx_coord(cls, cell: DocumentTableCell, axis: str, shape: Shape[float]) -> Tuple[int, float, int, float]:
        cell_coords = cls.bounding_regions_to_area(cell.bounding_regions, shape)
        if axis == "column":
            return cell.column_index, cell_coords.left, cell.column_index + cell.column_span, cell_coords.left + cell_coords.width
        return cell.row_index, cell_coords.top, cell.row_index + cell.row_span, cell_coords.top + cell_coords.height

    @classmethod
    def _get_axis_coordinates(cls, table: DocumentTable, axis: str, shape: Shape[float]) -> List[float]:
        cell2coord = dict()  # noqa: C408
        for cell in table.cells:
            min_idx, min_coord, max_idx, max_coord = cls._cell_to_idx_coord(cell, axis, shape)
            cell2coord[min_idx] = min_coord
            cell2coord[max_idx] = max_coord

        return cls.convert_idx2coord_to_coords(cell2coord)

    @staticmethod
    def bounding_regions_to_area(bounding_regions: List[BoundingRegion], shape: Shape[float]) -> RelativeAreaEntityWithPage:
        xs = []
        ys = []
        for bounding_region in bounding_regions:
            for point in bounding_region.polygon:
                xs.append(point.x)
                ys.append(point.y)
        min_x = min(xs)
        min_y = min(ys)
        max_x = max(xs)
        max_y = max(ys)
        return RelativeAreaEntityWithPage(
            left=min_x / shape.width,
            top=min_y / shape.height,
            width=(max_x - min_x) / shape.width,
            height=(max_y - min_y) / shape.height,
        )


class AzureModel(Enum):
    PREBUILT_LAYOUT = "prebuilt-layout"
    PREBUILT_DOCUMENT = "prebuilt-document"
    PREBUILT_INVOICE = "prebuilt-invoice"


class AzureTableExtractor(ITableExtractor):
    def __init__(
        self,
        azure_form_recognizer_api_url: str,
        azure_form_recognizer_api_key: str,
        ocr_service: OCRTableService,
    ):
        self._client = DocumentAnalysisClient(azure_form_recognizer_api_url, AzureKeyCredential(azure_form_recognizer_api_key))
        self._ocr_service = ocr_service

    def extract_tables(
        self,
        image_obj: ImageEntity,
        ocr_engine: str,
        language: str,
    ) -> List[TableEntity]:
        _logger.info("Starting table extraction with AzureTableExtractor")
        start = time.time()
        _, in_mem_bytes = cv2.imencode(".png", image_obj.image)
        poller = self._client.begin_analyze_document(AzureModel.PREBUILT_DOCUMENT.value, in_mem_bytes.tobytes())
        converted_tables: List[TableEntity] = AzureTableAdapter.convert_to_domain_table(
            poller.result(),
            image_obj.meta.source_id if image_obj.meta else None,
        )

        if ocr_engine in {AZURE_OCR_ENGINE, DEFAULT_OCR_ENGINE}:
            table_entities = converted_tables
        else:
            table_entities = [
                self._ocr_service.extract_data_from_table(image_obj, table, ocr_engine, language) for table in converted_tables
            ]
        _logger.info("Table extraction has completed %s seconds", round(time.time() - start, 3))
        return table_entities
