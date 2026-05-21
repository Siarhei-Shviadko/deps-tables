import json
import logging
import time
from typing import List, Optional, Tuple

import cv2
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from google.cloud.documentai_v1beta3.types import BoundingPoly, Document
from google.oauth2.service_account import Credentials

from deps_tables.domain.entities import (
    CellCoordinates,
    CellEntity,
    ColumnEntity,
    ImageEntity,
    RelativeAreaEntityWithPage,
    RowEntity,
    TableEntity,
)
from deps_tables.domain.exceptions import TablesException
from deps_tables.domain.interfaces import ITableAdapter, ITableExtractor
from deps_tables.domain.services import OCRTableService


class GCPTableAdapter(ITableAdapter):
    @classmethod
    def convert_to_domain_table(cls, document: Document, source_id: Optional[str] = None) -> List[TableEntity]:
        page: Document.Page = document.pages[0]
        tables: List[TableEntity] = []

        for table in page.tables:
            table_coordinates = cls.bounding_region_to_area(table.layout.bounding_poly)
            col_coords = cls._get_axis_coordinates(table, "column")
            row_coords = cls._get_axis_coordinates(table, "row")
            new_table = TableEntity(
                coordinates=table_coordinates,
                columns=cls.create_table_columns(col_coords, table_coordinates),
                rows=cls.create_table_rows(row_coords, table_coordinates),
                cells=cls.create_table_cells(table, col_coords, row_coords),
            )
            if source_id:
                new_table.fill_source_bbox_coordinates(source_id=source_id)
            tables.append(new_table)

        tables.sort(key=lambda x: (x.coordinates.top, x.coordinates.left))

        return tables

    @classmethod
    def create_table_columns(cls, col_coords: List[float], table_coordinates: RelativeAreaEntityWithPage) -> List[ColumnEntity]:
        rel_coords = cls.coords_to_relative(col_coords, table_coordinates.left, table_coordinates.width)
        return [ColumnEntity(x=max(0, x)) for x in rel_coords]

    @classmethod
    def create_table_rows(cls, row_coords: List[float], table_coordinates: RelativeAreaEntityWithPage) -> List[RowEntity]:
        rel_coords = cls.coords_to_relative(row_coords, table_coordinates.top, table_coordinates.height)
        return [RowEntity(y=max(0, y)) for y in rel_coords]

    @classmethod
    def _get_axis_coordinates(cls, table: Document.Page.Table, axis: str) -> List[float]:
        table_rows = list(table.header_rows) + list(table.body_rows)
        cell2coord = dict()  # noqa: C408
        for row_idx, row in enumerate(table_rows):
            for col_idx, cell in enumerate(row.cells):
                min_idx, min_coord, max_idx, max_coord = cls._cell_to_idx_coord(cell, axis, row_idx, col_idx)
                cell2coord[min_idx] = min_coord
                cell2coord[max_idx] = max_coord

        return cls.convert_idx2coord_to_coords(cell2coord)

    @classmethod
    def _cell_to_idx_coord(
        cls,
        cell: Document.Page.Table.TableCell,
        axis: str,
        row_idx: int,
        col_idx: int,
    ) -> Tuple[int, float, int, float]:
        cell_coords = cls.bounding_region_to_area(cell.layout.bounding_poly)
        if axis == "column":
            return col_idx, cell_coords.left, col_idx + cell.col_span, cell_coords.left + cell_coords.width
        return row_idx, cell_coords.top, row_idx + cell.row_span, cell_coords.top + cell_coords.height

    @classmethod
    def create_table_cells(cls, table: Document.Page.Table, col_coords: List[float], row_coords: List[float]) -> List[CellEntity]:
        cells: List[CellEntity] = []
        coord2col = {round(coord, 5): idx for idx, coord in enumerate(col_coords)}
        coord2row = {round(coord, 5): idx for idx, coord in enumerate(row_coords)}
        table_rows = list(table.header_rows) + list(table.body_rows)

        for row_index, row in enumerate(table_rows):
            for column_index, cell in enumerate(row.cells):
                cell_coords = cls.bounding_region_to_area(cell.layout.bounding_poly)
                cell_col_idx = coord2col.get(round(cell_coords.left, 5), column_index)
                cell_row_idx = coord2row.get(round(cell_coords.top, 5), row_index)
                cells.append(
                    CellEntity(
                        value=cell.layout.text_anchor.content,
                        coordinates=CellCoordinates(
                            column=cell_col_idx,
                            row=cell_row_idx,
                            column_span=cell.col_span,
                            row_span=cell.row_span,
                        ),
                    ),
                )

        return cells

    @classmethod
    def bounding_region_to_area(cls, bounding_poly: BoundingPoly) -> RelativeAreaEntityWithPage:
        xs = []
        ys = []
        for point in bounding_poly.normalized_vertices:
            xs.append(point.x)
            ys.append(point.y)
        min_x = min(xs)
        min_y = min(ys)
        max_x = max(xs)
        max_y = max(ys)
        return RelativeAreaEntityWithPage(
            left=min_x,
            top=min_y,
            width=max_x - min_x,
            height=max_y - min_y,
            page=1,
        )


class GCPTableExtractor(ITableExtractor):
    def __init__(
        self,
        gcp_project_id: str,
        gcp_location: str,
        gcp_processor_id: str,
        gcp_api_key: str,
        ocr_service: OCRTableService,
    ):
        self._ocr_service = ocr_service
        self._logger = logging.getLogger(__name__)

        client_options = ClientOptions(
            api_endpoint=f"{gcp_location}-documentai.googleapis.com",
        )

        self.client = documentai.DocumentProcessorServiceClient(
            client_options=client_options,
            credentials=self._get_credentials(gcp_api_key),
        )
        self.processor_resource_name = self.client.processor_path(
            gcp_project_id,
            gcp_location,
            gcp_processor_id,
        )

    def extract_tables(
        self,
        image_obj: ImageEntity,
        ocr_engine: str,
        language: str,
    ) -> List[TableEntity]:
        self._logger.info("Starting table extraction with GCPTableExtractor")

        start = time.time()

        _, in_mem_bytes = cv2.imencode(".png", image_obj.image)
        raw_document = documentai.RawDocument(content=in_mem_bytes.tobytes(), mime_type="image/png")
        request = documentai.ProcessRequest(name=self.processor_resource_name, raw_document=raw_document)

        response = self.client.process_document(request=request)

        converted_tables: List[TableEntity] = GCPTableAdapter.convert_to_domain_table(
            response.document,
            image_obj.meta.source_id if image_obj.meta else None,
        )
        table_entities = [
            self._ocr_service.extract_data_from_table(image_obj, table, ocr_engine, language) for table in converted_tables
        ]

        self._logger.info("Table extraction has completed %s seconds", round(time.time() - start, 3))

        return table_entities

    @staticmethod
    def _get_credentials(api_key: str) -> Credentials:
        try:
            json_data = json.loads(api_key)

        except json.JSONDecodeError:
            raise TablesException("Authorization key for GCP Document AI processor is invalid or missing")

        return Credentials.from_service_account_info(json_data)
