import logging
import time
from typing import Any, Dict, List, Optional, Tuple

import boto3
import cv2
from trp import BoundingBox
from trp import Cell as AWSCell
from trp import Document as AWSDocument
from trp import Table as AWSTable

from deps_tables.domain.constants import AWS_OCR_ENGINE, DEFAULT_OCR_ENGINE
from deps_tables.domain.entities import (
    CellCoordinates,
    CellEntity,
    ColumnEntity,
    ImageEntity,
    RelativeAreaEntityWithPage,
    RowEntity,
    TableEntity,
)
from deps_tables.domain.interfaces import ITableAdapter, ITableExtractor
from deps_tables.domain.services import OCRTableService

_logger = logging.getLogger(__name__)


class AWSTableAdapter(ITableAdapter):
    @classmethod
    def convert_to_domain_table(cls, recognized_forms: Dict[str, Any], source_id: Optional[str] = None) -> List[TableEntity]:
        page = AWSDocument(recognized_forms).pages[0]
        tables = []
        for table in page.tables:
            table_coordinates = cls.convert_bbox_to_area(table.geometry.boundingBox)
            new_table = TableEntity(
                coordinates=table_coordinates,
                columns=cls.create_columns(table, table_coordinates),
                rows=cls.create_rows(table, table_coordinates),
                cells=cls.create_cells(table),
            )
            if source_id:
                new_table.fill_source_bbox_coordinates(source_id)
            tables.append(new_table)

        tables.sort(key=lambda x: (x.coordinates.top, x.coordinates.left))

        return tables

    @classmethod
    def create_columns(cls, table: AWSTable, table_coordinates: RelativeAreaEntityWithPage) -> List[ColumnEntity]:
        col_coords = cls._get_axis_coordinates(table, "column")
        return [
            ColumnEntity(x=max(0, x)) for x in cls.coords_to_relative(col_coords, table_coordinates.left, table_coordinates.width)
        ]

    @classmethod
    def create_rows(cls, table: AWSTable, table_coordinates: RelativeAreaEntityWithPage) -> List[RowEntity]:
        row_coords = cls._get_axis_coordinates(table, "row")
        return [
            RowEntity(y=max(0, y)) for y in cls.coords_to_relative(row_coords, table_coordinates.top, table_coordinates.height)
        ]

    @classmethod
    def _get_axis_coordinates(cls, table: AWSTable, axis: str) -> List[float]:
        cell2coord = dict()  # noqa: C408
        for row in table.rows:
            for cell in row.cells:
                min_idx, min_coord, max_idx, max_coord = cls._cell_to_idx_coord(cell, axis)
                cell2coord[min_idx] = min_coord
                cell2coord[max_idx] = max_coord

        return cls.convert_idx2coord_to_coords(cell2coord)

    @classmethod
    def _cell_to_idx_coord(cls, cell: AWSCell, axis: str) -> Tuple[int, float, int, float]:
        cell_coords = cls.convert_bbox_to_area(cell.geometry.boundingBox)
        if axis == "column":
            return (
                cell.columnIndex - 1,
                cell_coords.left,
                cell.columnIndex + cell.columnSpan - 1,
                cell_coords.left + cell_coords.width,
            )
        return cell.rowIndex - 1, cell_coords.top, cell.rowIndex + cell.rowSpan - 1, cell_coords.top + cell_coords.height

    @classmethod
    def create_cells(cls, table: AWSTable) -> List[CellEntity]:
        cells = []
        for row in table.rows:
            for cell in row.cells:
                cells.append(
                    CellEntity(
                        value=cell.text,
                        coordinates=CellCoordinates(
                            column=cell.columnIndex - 1,
                            row=cell.rowIndex - 1,
                            column_span=cell.columnSpan,
                            row_span=cell.rowSpan,
                        ),
                        confidence=cell.confidence / 100,
                    ),
                )
        return cells

    @classmethod
    def convert_bbox_to_area(cls, bbox: BoundingBox) -> RelativeAreaEntityWithPage:
        return RelativeAreaEntityWithPage(
            left=bbox.left,
            top=bbox.top,
            width=bbox.width,
            height=bbox.height,
            page=1,
        )


class AWSTableExtractor(ITableExtractor):
    def __init__(
        self,
        aws_region_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        ocr_service: OCRTableService,
    ):
        self._textract_engine = boto3.client(
            "textract",
            region_name=aws_region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self._ocr_service = ocr_service

    def extract_tables(
        self,
        image_obj: ImageEntity,
        ocr_engine: str,
        language: str,
    ) -> List[TableEntity]:
        _logger.info("Starting table extraction with AWSTableExtractor")
        start = time.time()
        _, in_mem_bytes = cv2.imencode(".png", image_obj.image)
        response = self._textract_engine.analyze_document(Document={"Bytes": in_mem_bytes.tobytes()}, FeatureTypes=["TABLES"])
        converted_tables: List[TableEntity] = AWSTableAdapter.convert_to_domain_table(
            response,
            image_obj.meta.source_id if image_obj.meta else None,
        )

        if ocr_engine in {AWS_OCR_ENGINE, DEFAULT_OCR_ENGINE}:
            table_entities = converted_tables
        else:
            table_entities = [
                self._ocr_service.extract_data_from_table(image_obj, table, ocr_engine, language) for table in converted_tables
            ]
        _logger.info("Table extraction has completed %s seconds", round(time.time() - start, 3))
        return table_entities
