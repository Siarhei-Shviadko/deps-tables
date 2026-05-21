from typing import List, Optional

from pydantic import Field

from deps_tables.domain.entities import (
    CellCoordinates,
    CellEntity,
    ColumnEntity,
    RelativeAreaEntity,
    RelativeAreaEntityWithPage,
    RowEntity,
    SourceBboxCoordinates,
    TableEntity,
)

from .base import ConfiguredBaseModel
from .coordinates import (
    ColumnModel,
    RelativeAreaModel,
    RelativeAreaModelWithPage,
    RowModel,
)


class CellCoordinatesModel(ConfiguredBaseModel):
    column: int = Field(ge=0)
    row: int = Field(ge=0)
    column_span: int = Field(1, ge=1, alias="colspan")
    row_span: int = Field(1, ge=1, alias="rowspan")
    page: int = Field(1, ge=1)


class SourceBboxCoordinatesModel(ConfiguredBaseModel):
    source_id: str = Field(..., alias="sourceId")
    bboxes: List[RelativeAreaModel] = Field(default_factory=list)

    def to_domain(self) -> SourceBboxCoordinates:
        return SourceBboxCoordinates(
            source_id=self.source_id,
            bboxes=[RelativeAreaEntity(**bbox.dict()) for bbox in self.bboxes],
        )


class CellModel(ConfiguredBaseModel):
    value: Optional[str]
    coordinates: Optional[CellCoordinatesModel]
    confidence: Optional[float] = Field(1.0, ge=0, le=1.0)
    source_bbox_coordinates: List[SourceBboxCoordinatesModel] = Field(alias="sourceBboxCoordinates", default_factory=list)


class TableModel(ConfiguredBaseModel):
    columns: List[ColumnModel]
    rows: List[RowModel]
    cells: List[CellModel]
    coordinates: Optional[RelativeAreaModelWithPage]
    source_bbox_coordinates: Optional[SourceBboxCoordinatesModel] = Field(None, alias="sourceBboxCoordinates")

    def to_domain(self) -> TableEntity:
        return TableEntity(
            columns=[ColumnEntity(x=c.x) for c in self.columns],
            rows=[RowEntity(y=r.y) for r in self.rows],
            cells=[
                CellEntity(
                    value=cell.value,
                    coordinates=CellCoordinates(**cell.coordinates.dict()),
                    confidence=cell.confidence,
                    source_bbox_coordinates=[bb.to_domain() for bb in cell.source_bbox_coordinates],
                )
                for cell in self.cells
            ],
            coordinates=RelativeAreaEntityWithPage(**self.coordinates.dict()) if self.coordinates else None,
            source_bbox_coordinates=self.source_bbox_coordinates.to_domain() if self.source_bbox_coordinates else None,
        )
