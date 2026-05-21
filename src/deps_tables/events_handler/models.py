from typing import List

from pydantic import BaseModel, Field

from deps_tables.extras.ocr import BboxModel, TextLineModel, WordBoxModel


class ParsedBboxModel(BaseModel):
    y: float = Field(..., ge=0, le=1)
    x: float = Field(..., ge=0, le=1)
    w: float = Field(..., ge=0, le=1)
    h: float = Field(..., ge=0, le=1)


class ParsedWordBoxModel(BaseModel):
    value: str
    coordinates: ParsedBboxModel
    confidence: float = Field(1.0, ge=0, le=1)
    source_id: str = Field(..., alias="sourceId")


class ParsedTextLineModel(BaseModel):
    id: int
    word_boxes: List[ParsedWordBoxModel] = Field(..., alias="wordBoxes")

    def to_text_line_model(self) -> TextLineModel:
        return TextLineModel(
            id=self.id,
            word_boxes=[
                WordBoxModel(
                    content=box.value,
                    bbox=BboxModel(
                        x=box.coordinates.x,
                        y=box.coordinates.y,
                        w=box.coordinates.w,
                        h=box.coordinates.h,
                    ),
                    confidence=box.confidence,
                )
                for box in self.word_boxes
            ],
        )
