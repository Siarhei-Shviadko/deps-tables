from dataclasses import dataclass, field
from typing import List, Optional

from .coordinates import (
    ColumnEntity,
    RelativeAreaEntity,
    RelativeAreaEntityWithPage,
    RowEntity,
)


@dataclass
class CellCoordinates:
    column: int
    row: int
    column_span: int = 1
    row_span: int = 1
    page: int = 1


@dataclass
class SourceBboxCoordinates:
    source_id: str
    bboxes: List[RelativeAreaEntity]


@dataclass
class CellEntity:
    value: Optional[str] = None
    coordinates: Optional[CellCoordinates] = None
    confidence: Optional[float] = 1.0
    source_bbox_coordinates: List[SourceBboxCoordinates] = field(default_factory=list)


@dataclass
class TableEntity:
    cells: List[CellEntity]
    rows: List[RowEntity]
    columns: List[ColumnEntity]
    coordinates: Optional[RelativeAreaEntityWithPage] = None
    source_bbox_coordinates: Optional[SourceBboxCoordinates] = None

    def calculate_cell_global_coords(self, cell_coords: CellCoordinates) -> RelativeAreaEntity:
        def col_to_global_coords(col_idx):
            col_x = 1.0 if col_idx == len(self.columns) else self.columns[col_idx].x
            return self.coordinates.left + col_x * self.coordinates.width

        def row_to_global_coords(row_idx):
            row_y = 1.0 if row_idx == len(self.rows) else self.rows[row_idx].y
            return self.coordinates.top + row_y * self.coordinates.height

        top = row_to_global_coords(cell_coords.row)
        left = col_to_global_coords(cell_coords.column)

        return RelativeAreaEntity(
            top=top,
            left=left,
            height=row_to_global_coords(cell_coords.row + cell_coords.row_span) - top,
            width=col_to_global_coords(cell_coords.column + cell_coords.column_span) - left,
        )

    def fill_source_bbox_coordinates(self, source_id: str = "source_id"):
        self.source_bbox_coordinates = SourceBboxCoordinates(  # noqa: WPS601
            source_id=source_id,
            bboxes=[self.coordinates.to_relative_area()],
        )
        for cell in self.cells:
            cell.source_bbox_coordinates = [
                SourceBboxCoordinates(
                    source_id=source_id,
                    bboxes=[self.calculate_cell_global_coords(cell.coordinates)],
                ),
            ]
