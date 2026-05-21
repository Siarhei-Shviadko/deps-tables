from dataclasses import dataclass
from typing import Tuple

from deps_tables.domain.entities.geom import Rectangle, Shape
from deps_tables.domain.entities.ocr import PointEntity, RectangleEntity


class AbsoluteAreaEntity(Rectangle[int]):
    @classmethod
    def from_rect(cls, rect: Rectangle[int]) -> "AbsoluteAreaEntity":
        return cls(
            left=rect.left,
            top=rect.top,
            width=rect.width,
            height=rect.height,
        )

    def convert_to_global(self, outer: "AbsoluteAreaEntity") -> "AbsoluteAreaEntity":
        global_inner_rect = self.rect + outer.shift
        return self.from_rect(global_inner_rect)

    def convert_to_local(self, outer: "AbsoluteAreaEntity") -> "AbsoluteAreaEntity":
        local_inner_rect = self.rect - outer.shift
        return self.from_rect(local_inner_rect)


@dataclass
class BoundingBoxEntity(RectangleEntity):
    confidence: float

    @classmethod
    def from_tuple(cls, bbox: Tuple[Tuple[int, ...], float]) -> "BoundingBoxEntity":
        coords, confidence = bbox
        top_left = PointEntity(x=int(coords[0]), y=int(coords[1]))
        bottom_right = PointEntity(x=int(coords[2]), y=int(coords[3]))
        return cls(
            left_top_point=top_left,
            right_bottom_point=bottom_right,
            confidence=confidence,
        )


@dataclass
class RelativeAreaEntity:
    top: float
    left: float
    width: float
    height: float

    def to_absolute(self, shape: Shape[int]) -> AbsoluteAreaEntity:
        return AbsoluteAreaEntity(
            top=round(self.top * shape.height),
            left=round(self.left * shape.width),
            width=round(self.width * shape.width),
            height=round(self.height * shape.height),
        )

    @classmethod
    def from_absolute(cls, absolute: AbsoluteAreaEntity, shape: Shape[int]) -> "RelativeAreaEntity":
        return RelativeAreaEntity(
            top=absolute.top / shape.height,
            left=absolute.left / shape.width,
            width=absolute.width / shape.width,
            height=absolute.height / shape.height,
        )

    def to_global(self, outer: "RelativeAreaEntity") -> "RelativeAreaEntity":
        return RelativeAreaEntity(
            left=self.left * outer.width + outer.left,
            top=self.top * outer.height + outer.top,
            width=self.width * outer.width,
            height=self.height * outer.height,
        )


@dataclass
class RelativeAreaEntityWithPage(RelativeAreaEntity):
    page: int = 1

    def to_relative_area(self) -> RelativeAreaEntity:
        return RelativeAreaEntity(
            left=self.left,
            top=self.top,
            width=self.width,
            height=self.height,
        )

    def to_global(self, outer: RelativeAreaEntity) -> "RelativeAreaEntityWithPage":
        return RelativeAreaEntityWithPage(
            left=self.left * outer.width + outer.left,
            top=self.top * outer.height + outer.top,
            width=self.width * outer.width,
            height=self.height * outer.height,
            page=self.page,
        )


@dataclass
class RowEntity:
    y: float


@dataclass
class ColumnEntity:
    x: float
