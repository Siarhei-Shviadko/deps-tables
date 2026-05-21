import random
from itertools import product
from typing import List

import factory
from faker import Faker

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

faker = Faker()


class RelativeAreaFactory(factory.Factory):
    class Meta:
        model = RelativeAreaEntity

    left = random.uniform(0, 0.4)
    top = random.uniform(0, 0.4)
    width = random.uniform(0.1, 0.6)
    height = random.uniform(0.1, 0.6)


class RelativeAreaWithPageFactory(factory.Factory):
    class Meta:
        model = RelativeAreaEntityWithPage

    left = random.uniform(0, 0.4)
    top = random.uniform(0, 0.2)
    width = random.uniform(0.3, 0.6)
    height = random.uniform(0.2, 0.8)
    page = 1


class SourceBboxCoordinateFactory(factory.Factory):
    class Meta:
        model = SourceBboxCoordinates

    source_id = factory.Faker("uuid4")
    bboxes = factory.List([factory.SubFactory(RelativeAreaFactory) for _ in range(5)])


class CellFactory(factory.Factory):
    class Meta:
        model = CellEntity

    value = faker.sentence(nb_words=10)
    coordinates = None
    confidence = random.uniform(0, 1)
    source_bbox_coordinates = factory.List([factory.SubFactory(SourceBboxCoordinateFactory) for _ in range(5)])


class TableFactory(factory.Factory):
    class Meta:
        model = TableEntity

    columns = factory.LazyFunction(lambda: [ColumnEntity(x=value) for value in get_normalized_arr(random.randint(1, 3))])
    rows = factory.LazyFunction(lambda: [RowEntity(y=value) for value in get_normalized_arr(random.randint(1, 3))])
    cells = factory.LazyAttribute(
        lambda self: [
            CellFactory(coordinates=CellCoordinates(column=column, row=row))
            for row, column in product(range(len(self.rows)), range(len(self.columns)))
        ]
    )
    coordinates = factory.SubFactory(RelativeAreaWithPageFactory)
    source_bbox_coordinates = factory.SubFactory(SourceBboxCoordinateFactory)


def get_normalized_arr(n: int) -> List[float]:
    if n == 0:
        return []

    arr = [random.random() for _ in range(n)]
    s = sum(arr)
    arr = [x / s for x in arr]
    arr[0] = 0
    prev: float = 0
    for idx in range(len(arr)):
        arr[idx] += prev
        prev = arr[idx]

    return arr
