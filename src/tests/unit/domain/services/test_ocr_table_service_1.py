import mock
import numpy as np
import pytest

from deps_tables.api.models.table import TableModel
from deps_tables.domain.entities import (
    CellCoordinates,
    CellEntity,
    ColumnEntity,
    ImageEntity,
    PointEntity,
    RectangleEntity,
    RelativeAreaEntity,
    RelativeAreaEntityWithPage,
    RowEntity,
    SourceBboxCoordinates,
    TableEntity,
    TextLineEntity,
    WordBoxEntity,
)
from deps_tables.extras.ocr import Point, Rectangle, TextLine, WordBox
from tests.factories import TableFactory


class TestOCRTableService:
    @pytest.mark.parametrize("language", ["eng", "rus", "chi"])
    def test_extract_data_from_table__valid_data(self, ocr_table_service, language):
        table = TableFactory()
        image = ImageEntity(
            image=np.zeros((10, 10)),
            blob_path=None,
            meta=None,
        )
        text_lines = [
            TextLineEntity(
                id=1,
                word_boxes=[
                    WordBoxEntity(
                        content="value",
                        bbox=RectangleEntity(
                            left_top_point=PointEntity(x=0, y=0),
                            right_bottom_point=PointEntity(x=100, y=100),
                        ),
                    ),
                ],
            ),
        ]
        ocr_table_service._ocr_service.extract_data = mock.Mock(return_value=text_lines)

        ocr_table_service.extract_data_from_table(
            image=image,
            table=table,
            engine="TESSERACT",
            language=language,
        )

        ocr_table_service._ocr_service.extract_data.assert_called_with(
            image,
            "TESSERACT",
            language,
            mock.ANY,
        )


def test_extract_data_ocr_types_formatting(ocr_service):
    image = ImageEntity(
        image=np.zeros((10, 10)),
        blob_path=None,
        meta=None,
    )
    text_lines = [
        TextLine(
            id=1,
            word_boxes=[
                WordBox(
                    content="value",
                    bbox=Rectangle(
                        left_top_point=Point(x=0, y=0),
                        right_bottom_point=Point(x=5, y=5),
                    ),
                ),
                WordBox(
                    content="value2",
                    bbox=Rectangle(
                        left_top_point=Point(x=5, y=5),
                        right_bottom_point=Point(x=10, y=10),
                    ),
                ),
            ],
        ),
    ]
    text_line_entity_list = [
        TextLineEntity(
            id=1,
            word_boxes=[
                WordBoxEntity(
                    content="value",
                    bbox=RectangleEntity(
                        left_top_point=PointEntity(x=0, y=0),
                        right_bottom_point=PointEntity(x=5, y=5),
                    ),
                ),
                WordBoxEntity(
                    content="value2",
                    bbox=RectangleEntity(
                        left_top_point=PointEntity(x=5, y=5),
                        right_bottom_point=PointEntity(x=10, y=10),
                    ),
                ),
            ],
        ),
    ]
    ocr_service._ocr_service.extract_text = mock.Mock(return_value=text_lines)

    extracted_data = ocr_service.extract_data(
        image_obj=image,
        engine="TESSERACT",
        language="eng",
    )
    assert text_line_entity_list == extracted_data


def test_extract_data_from_table__formatting_ocr_types(ocr_table_service_with_ocr_service):
    table = TableFactory()
    image = ImageEntity(
        image=np.zeros((10, 10)),
        blob_path=None,
        meta=None,
    )
    text_lines = [
        TextLine(
            id=1,
            word_boxes=[
                WordBox(
                    content="value",
                    bbox=Rectangle(
                        left_top_point=Point(x=0, y=0),
                        right_bottom_point=Point(x=5, y=5),
                    ),
                ),
                WordBox(
                    content="value2",
                    bbox=Rectangle(
                        left_top_point=Point(x=5, y=5),
                        right_bottom_point=Point(x=10, y=10),
                    ),
                ),
            ],
        ),
    ]
    ocr_table_service_with_ocr_service._ocr_service._ocr_service.extract_text = mock.Mock(return_value=text_lines)
    extracted_table = ocr_table_service_with_ocr_service.extract_data_from_table(
        image=image,
        table=table,
        engine="TESSERACT",
        language="eng",
    )
    assert table == extracted_table


def test_extract_data_from_table__with_ocr_from_selected_area(ocr_table_service_with_ocr_service):

    table_json = {
        "rows": [{"y": 0}, {"y": 0.376470588235}],
        "columns": [{"x": 0}],
        "cells": [
            {
                "coordinates": {"row": 0, "column": 0, "rowspan": 1, "colspan": 1, "page": "1"},
                "value": "",
                "sourceBboxCoordinates": [
                    {
                        "sourceId": "de3481406ce24b39bf123f397536e37e",
                        "page": "1",
                        "bboxes": [
                            {"x": 0.7040983606557377, "y": 0.2242653015833922, "w": 0.2213114754098361, "h": 0.018545333986924095}
                        ],
                    }
                ],
            },
            {
                "coordinates": {"row": 1, "column": 0, "rowspan": 1, "colspan": 1, "page": "1"},
                "value": "",
                "sourceBboxCoordinates": [
                    {
                        "sourceId": "de3481406ce24b39bf123f397536e37e",
                        "page": "1",
                        "bboxes": [
                            {"x": 0.7040983606557377, "y": 0.2428106355703163, "w": 0.2213114754098361, "h": 0.03071570941584323}
                        ],
                    }
                ],
            },
        ],
        "coordinates": {
            "x": 0.7040983606557377,
            "y": 0.2242653015833922,
            "w": 0.2213114754098361,
            "h": 0.049261043402767324,
            "page": "1",
        },
        "source_bbox_coordinates": {
            "sourceId": "de3481406ce24b39bf123f397536e37e",
            "page": "1",
            "bboxes": [{"x": 0.7040983606557377, "y": 0.2242653015833922, "w": 0.2213114754098361, "h": 0.049261043402767324}],
        },
    }
    image = ImageEntity(
        image=np.zeros((2827, 2000)),
        blob_path=None,
        meta=None,
    )
    table_model = TableModel(**table_json)
    table = table_model.to_domain()

    text_lines = [
        TextLine(
            id=0,
            word_boxes=[
                WordBox(
                    content="Ala",
                    bbox=Rectangle(left_top_point=Point(x=15, y=14), right_bottom_point=Point(x=76, y=36)),
                    confidence=0.9170526885986328,
                ),
                WordBox(
                    content="Foods",
                    bbox=Rectangle(left_top_point=Point(x=89, y=14), right_bottom_point=Point(x=173, y=36)),
                    confidence=0.8990570068359375,
                ),
            ],
        ),
        TextLine(
            id=1,
            word_boxes=[
                WordBox(
                    content="52",
                    bbox=Rectangle(left_top_point=Point(x=15, y=70), right_bottom_point=Point(x=49, y=93)),
                    confidence=0.9220246124267578,
                ),
                WordBox(
                    content="USA",
                    bbox=Rectangle(left_top_point=Point(x=62, y=70), right_bottom_point=Point(x=145, y=93)),
                    confidence=0.9142926025390625,
                ),
                WordBox(
                    content="ABC",
                    bbox=Rectangle(left_top_point=Point(x=157, y=70), right_bottom_point=Point(x=275, y=93)),
                    confidence=0.9094705963134766,
                ),
                WordBox(
                    content="edf",
                    bbox=Rectangle(left_top_point=Point(x=286, y=70), right_bottom_point=Point(x=352, y=93)),
                    confidence=0.9197001647949219,
                ),
            ],
        ),
        TextLine(
            id=2,
            word_boxes=[
                WordBox(
                    content="August,",
                    bbox=Rectangle(left_top_point=Point(x=15, y=110), right_bottom_point=Point(x=111, y=138)),
                    confidence=0.8949707794189453,
                ),
                WordBox(
                    content="aaa",
                    bbox=Rectangle(left_top_point=Point(x=125, y=111), right_bottom_point=Point(x=170, y=133)),
                    confidence=0.9259485626220703,
                ),
                WordBox(
                    content="12345",
                    bbox=Rectangle(left_top_point=Point(x=182, y=110), right_bottom_point=Point(x=268, y=133)),
                    confidence=0.9539493560791016,
                ),
            ],
        ),
        TextLine(
            id=3,
            word_boxes=[
                WordBox(
                    content="Andrew",
                    bbox=Rectangle(left_top_point=Point(x=15, y=172), right_bottom_point=Point(x=125, y=195)),
                    confidence=0.9077790832519531,
                ),
                WordBox(
                    content="T",
                    bbox=Rectangle(left_top_point=Point(x=135, y=172), right_bottom_point=Point(x=152, y=195)),
                    confidence=0.9306066131591797,
                ),
                WordBox(
                    content="McGuire",
                    bbox=Rectangle(left_top_point=Point(x=164, y=172), right_bottom_point=Point(x=280, y=195)),
                    confidence=0.9179482269287109,
                ),
            ],
        ),
    ]

    ocr_table_service_with_ocr_service._ocr_service._ocr_service.extract_text = mock.Mock(return_value=text_lines)
    extracted_table = ocr_table_service_with_ocr_service.extract_data_from_table(
        image=image,
        table=table,
        engine="TESSERACT",
        language="eng",
    )
    ans_table = TableEntity(
        cells=[
            CellEntity(
                value="Ala Foods",
                coordinates=CellCoordinates(column=0, row=0, column_span=1, row_span=1, page=1),
                confidence=0.9080548477172852,
                source_bbox_coordinates=[
                    SourceBboxCoordinates(
                        source_id="de3481406ce24b39bf123f397536e37e",
                        bboxes=[
                            RelativeAreaEntity(
                                top=0.2242653015833922,
                                left=0.7040983606557377,
                                width=0.2213114754098361,
                                height=0.018545333986924095,
                            )
                        ],
                    )
                ],
            ),
            CellEntity(
                value="52 USA ABC edf August, aaa 12345",
                coordinates=CellCoordinates(column=0, row=1, column_span=1, row_span=1, page=1),
                confidence=0.9200509534563337,
                source_bbox_coordinates=[
                    SourceBboxCoordinates(
                        source_id="de3481406ce24b39bf123f397536e37e",
                        bboxes=[
                            RelativeAreaEntity(
                                top=0.2428106355703163,
                                left=0.7040983606557377,
                                width=0.2213114754098361,
                                height=0.03071570941584323,
                            )
                        ],
                    )
                ],
            ),
        ],
        rows=[RowEntity(y=0.0), RowEntity(y=0.376470588235)],
        columns=[ColumnEntity(x=0.0)],
        coordinates=RelativeAreaEntityWithPage(
            top=0.2242653015833922, left=0.7040983606557377, width=0.2213114754098361, height=0.049261043402767324, page=1
        ),
        source_bbox_coordinates=SourceBboxCoordinates(
            source_id="de3481406ce24b39bf123f397536e37e",
            bboxes=[
                RelativeAreaEntity(
                    top=0.2242653015833922, left=0.7040983606557377, width=0.2213114754098361, height=0.049261043402767324
                )
            ],
        ),
    )

    assert ans_table == extracted_table
