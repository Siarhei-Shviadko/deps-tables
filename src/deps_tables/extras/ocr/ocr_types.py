from typing import List

from pydantic import BaseModel, Field


class Point(BaseModel):
    x: int
    y: int


class Rectangle(BaseModel):
    left_top_point: Point
    right_bottom_point: Point


class WordBox(BaseModel):
    content: str
    bbox: Rectangle
    confidence: float = Field(1.0, ge=0.0, le=1.0)


class TextLine(BaseModel):
    id: int
    word_boxes: List[WordBox]
