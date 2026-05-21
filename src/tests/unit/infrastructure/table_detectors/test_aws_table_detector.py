import json
from dataclasses import asdict
from typing import Dict, List

import pytest
from trp import BoundingBox, Document

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
from deps_tables.infrastructure.table_extractors.aws_table_extractor import (
    AWSTableAdapter,
)


@pytest.fixture(scope="class")
def textract_raw_response_document():
    with open("tests/data/aws_resp2.json") as f:
        return json.load(f)


@pytest.fixture(scope="class")
def textract_response(textract_raw_response_document):
    return Document(textract_raw_response_document)


@pytest.fixture(scope="class")
def textract_table_response(textract_response):
    return textract_response.pages[0].tables[0]


@pytest.fixture
def table_area():
    return RelativeAreaEntityWithPage(
        left=0.08704297989606857, top=0.2787790894508362, width=0.8366580605506897, height=0.35116609930992126, page=1
    )


@pytest.fixture
def expected_columns() -> List[ColumnEntity]:
    return [
        ColumnEntity(x=x)
        for x in (
            0,
            0.3288770180624591,
            0.49732628564088677,
            0.6711230353685489,
            0.8315507057060684,
        )
    ]


@pytest.fixture
def expected_rows() -> List[RowEntity]:
    return [
        RowEntity(y=y)
        for y in (
            0,
            0.17539256596203792,
            0.2827224299995782,
            0.3743454970852942,
            0.4607329651870688,
            0.5680627443578681,
            0.6439790144917599,
            0.7356019967107349,
            0.8324607476471333,
            0.9450261258018741,
        )
    ]


@pytest.fixture
def expected_cells() -> List[CellEntity]:
    return [
        CellEntity(
            coordinates=CellCoordinates(column=x[0], row=x[1], column_span=x[2], row_span=x[3]), value=x[4], confidence=x[5]
        )
        for x in (
            (0, 0, 1, 1, "", 0.9999769592285156, 1.0),
            (1, 0, 1, 1, "truth ", 0.9999769592285156, 0.9998072052001953),
            (2, 0, 1, 1, "someone write ", 0.9999769592285156, 0.9997967910766602),
            (3, 0, 1, 1, "wide single on ", 0.9999769592285156, 0.9997378794352214),
            (4, 0, 1, 1, "account into same ", 0.9999769592285156, 0.9998310089111329),
            (
                0,
                1,
                1,
                1,
                "be computer wind together page bag staff ",
                0.9999769592285156,
                0.9993529728480748,
            ),
            (1, 1, 1, 1, "national country ", 0.9999769592285156, 0.9972786331176757),
            (2, 1, 1, 1, "discuss live ", 0.9999769592285156, 0.9844842529296876),
            (3, 1, 1, 1, "officer natural ", 0.9999769592285156, 0.9985869216918946),
            (4, 1, 1, 1, "at part ", 0.9999769592285156, 0.798659839630127),
            (
                0,
                2,
                1,
                1,
                "strategy teach international carry century wait leg ",
                0.9999769592285156,
                0.9997410147530692,
            ),
            (1, 2, 1, 1, "head ", 0.9999769592285156, 0.9788622283935546),
            (2, 2, 1, 1, "factor ", 0.9999769592285156, 0.9976740264892578),
            (3, 2, 1, 1, "teach ", 0.9999769592285156, 0.964246826171875),
            (4, 2, 1, 1, "there ", 0.9999769592285156, 0.9699638366699219),
            (
                0,
                3,
                1,
                1,
                "moment building world debate your ",
                0.9999769592285156,
                0.9946731567382813,
            ),
            (1, 3, 1, 1, "sell ", 0.9999769592285156, 0.9782728576660156),
            (2, 3, 1, 1, "action ", 0.9999769592285156, 0.9788560485839843),
            (3, 3, 1, 1, "cultural ", 0.9999769592285156, 0.9638043975830078),
            (4, 3, 1, 1, "contain ", 0.9999769592285156, 0.8961327362060547),
            (0, 4, 1, 1, "same on might ", 0.9999769592285156, 0.9996176656087239),
            (1, 4, 1, 1, "music ", 0.9999769592285156, 0.9820597076416016),
            (2, 4, 1, 1, "week ", 0.9999769592285156, 0.9561840057373047),
            (3, 4, 1, 1, "nature ", 0.9999769592285156, 0.9966855621337891),
            (4, 4, 1, 1, "development ", 0.9999769592285156, 0.9955968475341797),
            (
                0,
                5,
                1,
                1,
                "husband eight training represent red thought food ",
                0.9999769592285156,
                0.9990772138323102,
            ),
            (1, 5, 1, 1, "ask ", 0.9999769592285156, 0.9102626800537109),
            (2, 5, 1, 1, "try ", 0.9999769592285156, 0.9988796997070313),
            (3, 5, 1, 1, "town ", 0.9999769592285156, 0.9978744506835937),
            (4, 5, 1, 1, "region ", 0.9999769592285156, 0.9482801055908203),
            (
                0,
                6,
                1,
                1,
                "ability opportunity general field between store common ",
                0.9999769592285156,
                0.9997569710867745,
            ),
            (1, 6, 1, 1, "dream ", 0.9999769592285156, 0.9779219818115235),
            (2, 6, 1, 1, "challenge ", 0.9999769592285156, 0.9978030395507812),
            (3, 6, 1, 1, "wait ", 0.9999769592285156, 0.9975696563720703),
            (4, 6, 1, 1, "organization ", 0.9999769592285156, 0.9464085388183594),
            (
                0,
                7,
                1,
                1,
                "toward choose Republican wrong education ",
                0.9999769592285156,
                0.991742446899414,
            ),
            (1, 7, 1, 1, "dark ", 0.9999769592285156, 0.9979501342773438),
            (2, 7, 1, 1, "very ", 0.9999769592285156, 0.9841448211669922),
            (3, 7, 1, 1, "without ", 0.9999769592285156, 0.9834679412841797),
            (4, 7, 1, 1, "threat ", 0.9999769592285156, 0.9978701782226562),
            (
                0,
                8,
                1,
                1,
                "group establish serious ",
                0.9999769592285156,
                0.999633076985677,
            ),
            (1, 8, 1, 1, "player ", 0.9999769592285156, 0.9771070861816407),
            (2, 8, 1, 1, "investment ", 0.9999769592285156, 0.9790010070800781),
            (3, 8, 1, 1, "about ", 0.9999769592285156, 0.9979630279541015),
            (4, 8, 1, 1, "green ", 0.9999769592285156, 0.9983382415771485),
            (
                0,
                9,
                1,
                1,
                "another along billion pretty impact system early ",
                0.9999769592285156,
                0.9992483520507812,
            ),
            (1, 9, 1, 1, "us drug ", 0.9999769592285156, 0.9980643463134765),
            (2, 9, 1, 1, "guess son ", 0.9999769592285156, 0.9974549865722656),
            (3, 9, 1, 1, "police fund ", 0.9999769592285156, 0.9971531677246094),
            (4, 9, 1, 1, "strong accept ", 0.9999769592285156, 0.9962949752807617),
        )
    ]


@pytest.fixture
def expected_tables(table_area, expected_columns, expected_rows, expected_cells) -> List[TableEntity]:
    return [
        TableEntity(
            coordinates=table_area,
            columns=expected_columns,
            rows=expected_rows,
            cells=expected_cells,
        )
    ]


@pytest.fixture
def expected_cells_with_source_id(expected_cells) -> List[CellEntity]:
    expected_values_mapping = {
        (0, 0): (0.08704297989606857, 0.2787790894508362, 0.275157630443573, 0.06159194931387901),
        (1, 0): (0.3622005879878998, 0.2787790894508362, 0.14093440771102905, 0.06159194931387901),
        (2, 0): (0.5031350255012512, 0.2787790894508362, 0.14540845155715942, 0.06159194931387901),
        (3, 0): (0.6485434770584106, 0.2787790894508362, 0.13422314822673798, 0.06159194931387901),
        (4, 0): (0.782766580581665, 0.2787790894508362, 0.14093440771102905, 0.06159194931387901),
        (0, 1): (0.08704297989606857, 0.3403710126876831, 0.275157630443573, 0.03769060969352722),
        (1, 1): (0.3622005879878998, 0.3403710126876831, 0.14093440771102905, 0.03769060969352722),
        (2, 1): (0.5031350255012512, 0.3403710126876831, 0.14540845155715942, 0.03769060969352722),
        (3, 1): (0.6485434770584106, 0.3403710126876831, 0.13422314822673798, 0.03769060969352722),
        (4, 1): (0.782766580581665, 0.3403710126876831, 0.14093440771102905, 0.03769060969352722),
        (0, 2): (0.08704297989606857, 0.3780616223812103, 0.275157630443573, 0.03217490017414093),
        (1, 2): (0.3622005879878998, 0.3780616223812103, 0.14093440771102905, 0.03217490017414093),
        (2, 2): (0.5031350255012512, 0.3780616223812103, 0.14540845155715942, 0.03217490017414093),
        (3, 2): (0.6485434770584106, 0.3780616223812103, 0.13422314822673798, 0.03217490017414093),
        (4, 2): (0.782766580581665, 0.3780616223812103, 0.14093440771102905, 0.03217490017414093),
        (0, 3): (0.08704297989606857, 0.41023653745651245, 0.275157630443573, 0.03033634088933468),
        (1, 3): (0.3622005879878998, 0.41023653745651245, 0.14093440771102905, 0.03033634088933468),
        (2, 3): (0.5031350255012512, 0.41023653745651245, 0.14540845155715942, 0.03033634088933468),
        (3, 3): (0.6485434770584106, 0.41023653745651245, 0.13422314822673798, 0.03033634088933468),
        (4, 3): (0.782766580581665, 0.41023653745651245, 0.14093440771102905, 0.03033634088933468),
        (0, 4): (0.08704297989606857, 0.4405728876590729, 0.275157630443573, 0.03769060969352722),
        (1, 4): (0.3622005879878998, 0.4405728876590729, 0.14093440771102905, 0.03769060969352722),
        (2, 4): (0.5031350255012512, 0.4405728876590729, 0.14540845155715942, 0.03769060969352722),
        (3, 4): (0.6485434770584106, 0.4405728876590729, 0.13422314822673798, 0.03769060969352722),
        (4, 4): (0.782766580581665, 0.4405728876590729, 0.14093440771102905, 0.03769060969352722),
        (0, 5): (0.08704297989606857, 0.4782634675502777, 0.275157630443573, 0.026659199967980385),
        (1, 5): (0.3622005879878998, 0.4782634675502777, 0.14093440771102905, 0.026659199967980385),
        (2, 5): (0.5031350255012512, 0.4782634675502777, 0.14540845155715942, 0.026659199967980385),
        (3, 5): (0.6485434770584106, 0.4782634675502777, 0.13422314822673798, 0.026659199967980385),
        (4, 5): (0.782766580581665, 0.4782634675502777, 0.14093440771102905, 0.026659199967980385),
        (0, 6): (0.08704297989606857, 0.5049226880073547, 0.275157630443573, 0.03217490017414093),
        (1, 6): (0.3622005879878998, 0.5049226880073547, 0.14093440771102905, 0.03217490017414093),
        (2, 6): (0.5031350255012512, 0.5049226880073547, 0.14540845155715942, 0.03217490017414093),
        (3, 6): (0.6485434770584106, 0.5049226880073547, 0.13422314822673798, 0.03217490017414093),
        (4, 6): (0.782766580581665, 0.5049226880073547, 0.14093440771102905, 0.03217490017414093),
        (0, 7): (0.08704297989606857, 0.5370975732803345, 0.275157630443573, 0.03401349112391472),
        (1, 7): (0.3622005879878998, 0.5370975732803345, 0.14093440771102905, 0.03401349112391472),
        (2, 7): (0.5031350255012512, 0.5370975732803345, 0.14540845155715942, 0.03401349112391472),
        (3, 7): (0.6485434770584106, 0.5370975732803345, 0.13422314822673798, 0.03401349112391472),
        (4, 7): (0.782766580581665, 0.5370975732803345, 0.14093440771102905, 0.03401349112391472),
        (0, 8): (0.08704297989606857, 0.5711110830307007, 0.275157630443573, 0.039529189467430115),
        (1, 8): (0.3622005879878998, 0.5711110830307007, 0.14093440771102905, 0.039529189467430115),
        (2, 8): (0.5031350255012512, 0.5711110830307007, 0.14540845155715942, 0.039529189467430115),
        (3, 8): (0.6485434770584106, 0.5711110830307007, 0.13422314822673798, 0.039529189467430115),
        (4, 8): (0.782766580581665, 0.5711110830307007, 0.14093440771102905, 0.039529189467430115),
        (0, 9): (0.08704297989606857, 0.6106402277946472, 0.275157630443573, 0.0193049106746912),
        (1, 9): (0.3622005879878998, 0.6106402277946472, 0.14093440771102905, 0.0193049106746912),
        (2, 9): (0.5031350255012512, 0.6106402277946472, 0.14540845155715942, 0.0193049106746912),
        (3, 9): (0.6485434770584106, 0.6106402277946472, 0.13422314822673798, 0.0193049106746912),
        (4, 9): (0.782766580581665, 0.6106402277946472, 0.14093440771102905, 0.0193049106746912),
    }
    for cell in expected_cells:
        bbox_values = expected_values_mapping[(cell.coordinates.column, cell.coordinates.row)]
        bbox = RelativeAreaEntity(left=bbox_values[0], top=bbox_values[1], width=bbox_values[2], height=bbox_values[3])
        cell.source_bbox_coordinates = [SourceBboxCoordinates(source_id="source_id", bboxes=[bbox])]
    return expected_cells


@pytest.fixture
def expected_tables_with_source_id(table_area, expected_tables, expected_cells_with_source_id) -> List[TableEntity]:
    expected_tables[0].source_bbox_coordinates = SourceBboxCoordinates(
        source_id="source_id", bboxes=[table_area.to_relative_area()]
    )
    expected_tables[0].cells = expected_cells_with_source_id
    return expected_tables


class TestAWSAdapter:
    def test_convert_bounding_box_to_area__return_relative_area(self):
        bbox = BoundingBox(
            width=0.275157630443573,
            height=0.06159194931387901,
            left=0.08704297989606857,
            top=0.2787790894508362,
        )
        expected_relative_area = RelativeAreaEntityWithPage(
            left=0.08704297989606857,
            top=0.2787790894508362,
            width=0.275157630443573,
            height=0.06159194931387901,
        )

        assert expected_relative_area == AWSTableAdapter.convert_bbox_to_area(bbox)

    def test_create_table_columns__return_columns_list(self, textract_table_response, table_area, expected_columns):
        columns = AWSTableAdapter.create_columns(textract_table_response, table_area)
        assert columns == expected_columns

    def test_create_table_rows__return_rows_list(self, textract_table_response, table_area, expected_rows):
        rows = AWSTableAdapter.create_rows(textract_table_response, table_area)
        assert rows == expected_rows

    def test_create_table_cells__return_cells_list(self, textract_table_response, expected_cells):
        cells = AWSTableAdapter.create_cells(textract_table_response)
        assert cells == expected_cells

    def test_convert_to_domain_table__return_one_table(self, textract_raw_response_document):
        tables = AWSTableAdapter.convert_to_domain_table(
            recognized_forms=textract_raw_response_document,
            source_id=None,
        )

        assert len(tables) == 1

    def test_convert_to_domain_table__no_source_id__return_table(self, textract_raw_response_document, expected_tables):
        tables = AWSTableAdapter.convert_to_domain_table(
            recognized_forms=textract_raw_response_document,
            source_id=None,
        )
        assert tables == expected_tables

    def test_convert_to_domain_table__source_id_exists__return_table(
        self, textract_raw_response_document, expected_tables_with_source_id
    ):
        def rounded_coords(coords: SourceBboxCoordinates) -> Dict:
            return {k: round(v, 5) for (k, v) in asdict(coords.bboxes[0]).items()}

        def near_equal(coords1: SourceBboxCoordinates, coords2: SourceBboxCoordinates) -> bool:
            return rounded_coords(coords1) == rounded_coords(coords2)

        tables = AWSTableAdapter.convert_to_domain_table(
            recognized_forms=textract_raw_response_document,
            source_id="source_id",
        )
        assert len(tables[0].cells) == len(expected_tables_with_source_id[0].cells)
        assert all(
            near_equal(cell.source_bbox_coordinates[0], expected_cell.source_bbox_coordinates[0])
            for (cell, expected_cell) in zip(tables[0].cells, expected_tables_with_source_id[0].cells)
        )
        for cell in tables[0].cells:
            cell.source_bbox_coordinates = []
        for cell in expected_tables_with_source_id[0].cells:
            cell.source_bbox_coordinates = []
        assert tables[0].source_bbox_coordinates == expected_tables_with_source_id[0].source_bbox_coordinates
        assert tables == expected_tables_with_source_id
