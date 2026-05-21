import pytest

from deps_tables.domain.entities.geom import Shape

FIXME = """
Currently there are problems with rounding, so absolute -> relative -> absolute conversion leads to losing pixels
"""


@pytest.fixture
def shape():
    return Shape(width=2000, height=1500)
