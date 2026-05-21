import pytest

from deps_tables.domain.entities.geom import Rectangle, Vector2d


class TestGeomPrimitivies:
    def test_vector_math(self) -> None:
        vec1 = Vector2d(x=4, y=6)
        vec2 = Vector2d(x=1, y=2)

        assert vec1 + vec2 == Vector2d(x=5, y=8)
        assert vec2 + vec1 == Vector2d(x=5, y=8)
        assert -vec1 == Vector2d(x=-4, y=-6)
        assert vec1 - vec2 == Vector2d(x=3, y=4)
        assert vec2 - vec1 == Vector2d(x=-3, y=-4)

    def test_rectangle_math(self) -> None:
        rect = Rectangle(left=1, top=2, width=3, height=4)

        assert rect.right == 4
        assert rect.bottom == 6
        assert rect.shift == Vector2d(x=1, y=2)

        vec = Vector2d(x=5, y=6)
        assert rect + vec == Rectangle(left=6, top=8, width=3, height=4)
