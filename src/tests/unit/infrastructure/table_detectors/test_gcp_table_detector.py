import pickle
from dataclasses import asdict
from typing import Dict

import pytest
from google.cloud.documentai_v1beta3.types import BoundingPoly, NormalizedVertex, Vertex

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
from deps_tables.infrastructure.table_extractors.gcp_table_extractor import (
    GCPTableAdapter,
)


@pytest.fixture(scope="class")
def gcp_response():
    with open("tests/data/gcp_resp.pickle", "rb") as f:
        return pickle.load(f)


@pytest.fixture(scope="class")
def gcp_response_table(gcp_response):
    return gcp_response.document.pages[0].tables[0]


@pytest.fixture()
def expected_columns_coordinates():
    return [
        0,
        0.06720977276563644,
        0.6456211805343628,
        0.8350305557250977,
    ]


@pytest.fixture
def expected_columns():
    return [
        ColumnEntity(x=x)
        for x in (
            0,
            0.06860706606136793,
            0.6590436652418867,
            0.8523908673171967,
        )
    ]


@pytest.fixture()
def expected_rows_coordinates():
    return [
        0.048076923936605453,
        0.11057692021131516,
        0.2740384638309479,
        0.3413461446762085,
        0.3990384638309479,
        0.45673078298568726,
        0.5192307829856873,
        0.5769230723381042,
        0.6394230723381042,
        0.6971153616905212,
        0.7596153616905212,
        0.817307710647583,
        0.875,
        0.932692289352417,
    ]


@pytest.fixture
def expected_rows():
    return [
        RowEntity(y=y)
        for y in (
            0,
            0.06598984512015636,
            0.2385786865522329,
            0.30964466573810595,
            0.37055838465914864,
            0.43147210358019134,
            0.49746195263364923,
            0.5583756400882798,
            0.6243654891417377,
            0.6852791765963683,
            0.7512690256498261,
            0.812182776037281,
            0.8730964634919115,
            0.9340101509465422,
        )
    ]


@pytest.fixture
def expected_cells():
    return [
        CellEntity(coordinates=CellCoordinates(column=x[0], row=x[1], column_span=x[2], row_span=x[3]), value=x[4])
        for x in (
            (0, 0, 1, 1, ""),
            (1, 0, 1, 1, ""),
            (2, 0, 1, 1, ""),
            (3, 0, 1, 1, ""),
            (0, 1, 1, 1, ""),
            (1, 1, 1, 1, ""),
            (2, 1, 1, 1, ""),
            (3, 1, 1, 1, ""),
            (0, 2, 1, 1, ""),
            (1, 2, 1, 1, ""),
            (2, 2, 1, 1, ""),
            (3, 2, 1, 1, ""),
            (0, 3, 1, 1, ""),
            (1, 3, 1, 1, ""),
            (2, 3, 1, 1, ""),
            (3, 3, 1, 1, ""),
            (0, 4, 1, 1, ""),
            (1, 4, 1, 1, ""),
            (2, 4, 1, 1, ""),
            (3, 4, 1, 1, ""),
            (0, 5, 1, 1, ""),
            (1, 5, 1, 1, ""),
            (2, 5, 1, 1, ""),
            (3, 5, 1, 1, ""),
            (0, 6, 1, 1, ""),
            (1, 6, 1, 1, ""),
            (2, 6, 1, 1, ""),
            (3, 6, 1, 1, ""),
            (0, 7, 1, 1, ""),
            (1, 7, 1, 1, ""),
            (2, 7, 1, 1, ""),
            (3, 7, 1, 1, ""),
            (0, 8, 1, 1, ""),
            (1, 8, 1, 1, ""),
            (2, 8, 1, 1, ""),
            (3, 8, 1, 1, ""),
            (0, 9, 1, 1, ""),
            (1, 9, 1, 1, ""),
            (2, 9, 1, 1, ""),
            (3, 9, 1, 1, ""),
            (0, 10, 1, 1, ""),
            (1, 10, 1, 1, ""),
            (2, 10, 1, 1, ""),
            (3, 10, 1, 1, ""),
            (0, 11, 1, 1, ""),
            (1, 11, 1, 1, ""),
            (2, 11, 1, 1, ""),
            (3, 11, 1, 1, ""),
            (0, 12, 1, 1, ""),
            (1, 12, 1, 1, ""),
            (2, 12, 1, 1, ""),
            (3, 12, 1, 1, ""),
            (0, 13, 1, 1, ""),
            (1, 13, 1, 1, ""),
            (2, 13, 1, 1, ""),
            (3, 13, 1, 1, ""),
        )
    ]


@pytest.fixture
def table_area():
    return RelativeAreaEntityWithPage(
        left=0,
        top=0.048076923936605453,
        width=0.9796333909034729,
        height=0.9471153654158115,
    )


@pytest.fixture
def expected_table(expected_rows, expected_columns, expected_cells, table_area):
    return TableEntity(
        cells=expected_cells,
        rows=expected_rows,
        columns=expected_columns,
        coordinates=table_area,
    )


@pytest.fixture
def expected_table_with_source_id(expected_table):
    mapping = {
        (0, 0): (0, 0.048076923936605453, 0.06720977276563644, 0.0624999962747097),
        (1, 0): (0.06720977276563644, 0.048076923936605453, 0.5784114077687263, 0.0624999962747097),
        (2, 0): (0.6456211805343628, 0.048076923936605453, 0.18940937519073486, 0.0624999962747097),
        (3, 0): (0.8350305557250977, 0.048076923936605453, 0.14460283517837524, 0.0624999962747097),
        (0, 1): (0, 0.11057692021131516, 0.06720977276563644, 0.16346154361963272),
        (1, 1): (0.06720977276563644, 0.11057692021131516, 0.5784114077687263, 0.16346154361963272),
        (2, 1): (0.6456211805343628, 0.11057692021131516, 0.18940937519073486, 0.16346154361963272),
        (3, 1): (0.8350305557250977, 0.11057692021131516, 0.14460283517837524, 0.16346154361963272),
        (0, 2): (0, 0.2740384638309479, 0.06720977276563644, 0.06730768084526062),
        (1, 2): (0.06720977276563644, 0.2740384638309479, 0.5784114077687263, 0.06730768084526062),
        (2, 2): (0.6456211805343628, 0.2740384638309479, 0.18940937519073486, 0.06730768084526062),
        (3, 2): (0.8350305557250977, 0.2740384638309479, 0.14460283517837524, 0.06730768084526062),
        (0, 3): (0, 0.3413461446762085, 0.06720977276563644, 0.05769231915473938),
        (1, 3): (0.06720977276563644, 0.3413461446762085, 0.5784114077687263, 0.05769231915473938),
        (2, 3): (0.6456211805343628, 0.3413461446762085, 0.18940937519073486, 0.05769231915473938),
        (3, 3): (0.8350305557250977, 0.3413461446762085, 0.14460283517837524, 0.05769231915473938),
        (0, 4): (0, 0.3990384638309479, 0.06720977276563644, 0.05769231915473938),
        (1, 4): (0.06720977276563644, 0.3990384638309479, 0.5784114077687263, 0.05769231915473938),
        (2, 4): (0.6456211805343628, 0.3990384638309479, 0.18940937519073486, 0.05769231915473938),
        (3, 4): (0.8350305557250977, 0.3990384638309479, 0.14460283517837524, 0.05769231915473938),
        (0, 5): (0, 0.45673078298568726, 0.06720977276563644, 0.0625),
        (1, 5): (0.06720977276563644, 0.45673078298568726, 0.5784114077687263, 0.0625),
        (2, 5): (0.6456211805343628, 0.45673078298568726, 0.18940937519073486, 0.0625),
        (3, 5): (0.8350305557250977, 0.45673078298568726, 0.14460283517837524, 0.0625),
        (0, 6): (0, 0.5192307829856873, 0.06720977276563644, 0.05769228935241699),
        (1, 6): (0.06720977276563644, 0.5192307829856873, 0.5784114077687263, 0.05769228935241699),
        (2, 6): (0.6456211805343628, 0.5192307829856873, 0.18940937519073486, 0.05769228935241699),
        (3, 6): (0.8350305557250977, 0.5192307829856873, 0.14460283517837524, 0.05769228935241699),
        (0, 7): (0, 0.5769230723381042, 0.06720977276563644, 0.0625),
        (1, 7): (0.06720977276563644, 0.5769230723381042, 0.5784114077687263, 0.0625),
        (2, 7): (0.6456211805343628, 0.5769230723381042, 0.18940937519073486, 0.0625),
        (3, 7): (0.8350305557250977, 0.5769230723381042, 0.14460283517837524, 0.0625),
        (0, 8): (0, 0.6394230723381042, 0.06720977276563644, 0.05769228935241699),
        (1, 8): (0.06720977276563644, 0.6394230723381042, 0.5784114077687263, 0.05769228935241699),
        (2, 8): (0.6456211805343628, 0.6394230723381042, 0.18940937519073486, 0.05769228935241699),
        (3, 8): (0.8350305557250977, 0.6394230723381042, 0.14460283517837524, 0.05769228935241699),
        (0, 9): (0, 0.6971153616905212, 0.06720977276563644, 0.0625),
        (1, 9): (0.06720977276563644, 0.6971153616905212, 0.5784114077687263, 0.0625),
        (2, 9): (0.6456211805343628, 0.6971153616905212, 0.18940937519073486, 0.0625),
        (3, 9): (0.8350305557250977, 0.6971153616905212, 0.14460283517837524, 0.0625),
        (0, 10): (0, 0.7596153616905212, 0.06720977276563644, 0.05769234895706177),
        (1, 10): (0.06720977276563644, 0.7596153616905212, 0.5784114077687263, 0.05769234895706177),
        (2, 10): (0.6456211805343628, 0.7596153616905212, 0.18940937519073486, 0.05769234895706177),
        (3, 10): (0.8350305557250977, 0.7596153616905212, 0.14460283517837524, 0.05769234895706177),
        (0, 11): (0, 0.817307710647583, 0.06720977276563644, 0.05769228935241699),
        (1, 11): (0.06720977276563644, 0.817307710647583, 0.5784114077687263, 0.05769228935241699),
        (2, 11): (0.6456211805343628, 0.817307710647583, 0.18940937519073486, 0.05769228935241699),
        (3, 11): (0.8350305557250977, 0.817307710647583, 0.14460283517837524, 0.05769228935241699),
        (0, 12): (0, 0.875, 0.06720977276563644, 0.05769228935241699),
        (1, 12): (0.06720977276563644, 0.875, 0.5784114077687263, 0.05769228935241699),
        (2, 12): (0.6456211805343628, 0.875, 0.18940937519073486, 0.05769228935241699),
        (3, 12): (0.8350305557250977, 0.875, 0.14460283517837524, 0.05769228935241699),
        (0, 13): (0, 0.932692289352417, 0.06720977276563644, 0.0625),
        (1, 13): (0.06720977276563644, 0.932692289352417, 0.5784114077687263, 0.0625),
        (2, 13): (0.6456211805343628, 0.932692289352417, 0.18940937519073486, 0.0625),
        (3, 13): (0.8350305557250977, 0.932692289352417, 0.14460283517837524, 0.0625),
    }
    for cell in expected_table.cells:
        bbox_values = mapping[(cell.coordinates.column, cell.coordinates.row)]
        bbox = RelativeAreaEntity(left=bbox_values[0], top=bbox_values[1], width=bbox_values[2], height=bbox_values[3])
        cell.source_bbox_coordinates = [SourceBboxCoordinates(source_id="source_id", bboxes=[bbox])]
    expected_table.source_bbox_coordinates = SourceBboxCoordinates(
        source_id="source_id", bboxes=[expected_table.coordinates.to_relative_area()]
    )
    return expected_table


class TestGCPTableAdapter:
    def test_bounding_region_to_area__return_relative_area(self):
        bounding_poly = BoundingPoly(
            vertices=[Vertex(x=0, y=10), Vertex(x=33, y=10), Vertex(x=33, y=23), Vertex(x=0, y=23)],
            normalized_vertices=[
                NormalizedVertex(x=0, y=0.048076923936605453),
                NormalizedVertex(x=0.06720977276563644, y=0.048076923936605453),
                NormalizedVertex(x=0.06720977276563644, y=0.11057692021131516),
                NormalizedVertex(x=0, y=0.11057692021131516),
            ],
        )
        expected_relative_area = RelativeAreaEntityWithPage(
            left=0,
            top=0.048076923936605453,
            width=0.06720977276563644,
            height=0.0624999962747097,
        )
        assert expected_relative_area == GCPTableAdapter.bounding_region_to_area(bounding_poly)

    def test__get_axis_coordinates_return_columns(self, gcp_response_table, expected_columns_coordinates):
        assert expected_columns_coordinates == GCPTableAdapter._get_axis_coordinates(gcp_response_table, "column")

    def test__get_axis_coordinates_return_rows(self, gcp_response_table, expected_rows_coordinates):
        assert expected_rows_coordinates == GCPTableAdapter._get_axis_coordinates(gcp_response_table, "row")

    def test_create_table_columns__return_columns_list(self, expected_columns_coordinates, table_area, expected_columns):
        columns = GCPTableAdapter.create_table_columns(expected_columns_coordinates, table_area)

        assert columns == expected_columns

    def test_create_table_rows__return_rows_list(self, expected_rows_coordinates, table_area, expected_rows):
        rows = GCPTableAdapter.create_table_rows(expected_rows_coordinates, table_area)

        assert rows == expected_rows

    def test_create_table_cells__return_cells_list(
        self,
        gcp_response_table,
        expected_columns_coordinates,
        expected_rows_coordinates,
        expected_cells,
    ):
        cells = GCPTableAdapter.create_table_cells(gcp_response_table, expected_columns_coordinates, expected_rows_coordinates)

        assert cells == expected_cells

    def test_convert_to_domain_tables__no_source_id__return_proper_table(self, gcp_response, expected_table):
        tables = GCPTableAdapter.convert_to_domain_table(document=gcp_response.document)

        assert tables == [expected_table]

    def test_convert_to_domain_tables__source_id_return_proper_table(
        self, gcp_response, expected_table_with_source_id, expected_columns_coordinates, expected_rows_coordinates
    ):
        def rounded_coords(coords: SourceBboxCoordinates) -> Dict:
            return {k: round(v, 5) for (k, v) in asdict(coords.bboxes[0]).items()}

        def near_equal(coords1: SourceBboxCoordinates, coords2: SourceBboxCoordinates) -> bool:
            return rounded_coords(coords1) == rounded_coords(coords2)

        tables = GCPTableAdapter.convert_to_domain_table(document=gcp_response.document, source_id="source_id")

        assert len(tables[0].cells) == len(expected_table_with_source_id.cells)
        assert all(
            near_equal(cell.source_bbox_coordinates[0], expected_cell.source_bbox_coordinates[0])
            for (cell, expected_cell) in zip(tables[0].cells, expected_table_with_source_id.cells)
        )
        for cell in tables[0].cells:
            cell.source_bbox_coordinates = []
        for cell in expected_table_with_source_id.cells:
            cell.source_bbox_coordinates = []
        assert tables[0].source_bbox_coordinates == expected_table_with_source_id.source_bbox_coordinates
        assert tables == [expected_table_with_source_id]
