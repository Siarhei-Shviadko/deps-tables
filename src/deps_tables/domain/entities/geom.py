from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T", int, float)


@dataclass
class Vector2d(Generic[T]):
    x: T
    y: T

    def __add__(self, other: "Vector2d[T]") -> "Vector2d[T]":
        if isinstance(other, Vector2d):
            return Vector2d(
                x=self.x + other.x,
                y=self.y + other.y,
            )

        raise NotImplementedError

    def __sub__(self, other: "Vector2d[T]") -> "Vector2d[T]":
        if isinstance(other, Vector2d):
            return self + (-other)  # noqa: WPS346

        raise NotImplementedError

    def __neg__(self) -> "Vector2d[T]":
        return Vector2d(
            x=-self.x,
            y=-self.y,
        )

    def __rsub__(self, other):
        return other + (-self)  # noqa: WPS346

    def __radd__(self, other):
        return other + self


@dataclass
class Shape(Generic[T]):
    width: T
    height: T


Shift = Vector2d


@dataclass
class Rectangle(Generic[T]):
    left: T
    top: T
    width: T
    height: T

    @property
    def right(self) -> T:
        return self.left + self.width

    @property
    def bottom(self) -> T:
        return self.top + self.height

    @property
    def rect(self) -> "Rectangle[T]":
        return Rectangle(
            left=self.left,
            top=self.top,
            width=self.width,
            height=self.height,
        )

    def __add__(self, other: Vector2d[T]) -> "Rectangle[T]":
        return Rectangle(
            left=self.left + other.x,
            top=self.top + other.y,
            width=self.width,
            height=self.height,
        )

    @property
    def shift(self) -> Shift[T]:
        return Vector2d(
            x=self.left,
            y=self.top,
        )

    @property
    def shape(self) -> Shape[T]:
        return Shape(
            width=self.width,
            height=self.height,
        )
