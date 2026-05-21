from dataclasses import dataclass
from typing import List

from deps_tables.extras.ocr import Point, TextLine


@dataclass
class PointEntity:
    x: int
    y: int

    @staticmethod
    def from_domain(point: Point) -> "PointEntity":
        return PointEntity(point.x, point.y)


@dataclass
class RectangleEntity:
    left_top_point: PointEntity
    right_bottom_point: PointEntity

    def intersects_with(self, other: "RectangleEntity", *, threshold: float = 0.65) -> bool:
        if not isinstance(other, self.__class__):
            return False
        self_left, other_left = (min(rect.left_top_point.x, rect.right_bottom_point.x) for rect in (self, other))
        self_right, other_right = (max(rect.left_top_point.x, rect.right_bottom_point.x) for rect in (self, other))
        self_top, other_top = (max(rect.left_top_point.y, rect.right_bottom_point.y) for rect in (self, other))
        self_bottom, other_bottom = (min(rect.left_top_point.y, rect.right_bottom_point.y) for rect in (self, other))

        inner_height = max(0, min(self_top, other_top) - max(self_bottom, other_bottom))
        inner_width = max(0, min(self_right, other_right) - max(self_left, other_left))
        inner_square = inner_width * inner_height

        self_square = (self_top - self_bottom) * (self_right - self_left)
        other_square = (other_top - other_bottom) * (other_right - other_left)

        try:
            intersection_rate = inner_square / min(self_square, other_square)
        except ZeroDivisionError:
            intersection_rate = 0
        return intersection_rate >= threshold

    def is_inside(self, other: "RectangleEntity") -> bool:
        if not isinstance(other, self.__class__):
            return False

        if not (
            min(self.right_bottom_point.x, other.right_bottom_point.x) > max(self.left_top_point.x, other.left_top_point.x)
            and min(self.right_bottom_point.y, other.right_bottom_point.y) > max(self.left_top_point.y, other.left_top_point.y)
        ):
            return False
        x_center = (self.left_top_point.x + self.right_bottom_point.x) / 2
        y_center = (self.left_top_point.y + self.right_bottom_point.y) / 2
        return (other.left_top_point.x <= x_center <= other.right_bottom_point.x) and (
            other.left_top_point.y <= y_center <= other.right_bottom_point.y
        )


@dataclass
class WordBoxEntity:
    content: str
    bbox: RectangleEntity
    confidence: float = 1.0


@dataclass
class TextLineEntity:
    id: int
    word_boxes: List[WordBoxEntity]

    @staticmethod
    def from_domain(text_line: TextLine) -> "TextLineEntity":
        return TextLineEntity(
            id=text_line.id,
            word_boxes=[
                WordBoxEntity(
                    content=word_box.content,
                    bbox=RectangleEntity(
                        left_top_point=PointEntity.from_domain(word_box.bbox.left_top_point),
                        right_bottom_point=PointEntity.from_domain(word_box.bbox.right_bottom_point),
                    ),
                    confidence=word_box.confidence,
                )
                for word_box in text_line.word_boxes
            ],
        )
