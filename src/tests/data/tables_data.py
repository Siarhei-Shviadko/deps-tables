from matplotlib.widgets import TextBox

from deps_tables.api.models.table import TableModel
from deps_tables.domain.entities import (
    PointEntity,
    RectangleEntity,
    TextLineEntity,
    WordBoxEntity,
)

tables_data = [
    {
        "rows": [
            {"y": 0.0093240093},
            {"y": 0.1445221445},
            {"y": 0.2820512821},
            {"y": 0.4172494172},
            {"y": 0.5524475524},
            {"y": 0.6876456876},
            {"y": 0.8228438228},
        ],
        "cells": [
            {
                "value": " ads",
                "confidence": 1.0,
                "coordinates": {
                    "row": 0,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " adsda",
                "confidence": 1.0,
                "coordinates": {
                    "row": 1,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 2,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 3,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 4,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 5,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 6,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " 13212",
                "confidence": 1.0,
                "coordinates": {
                    "row": 0,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " adsda",
                "confidence": 1.0,
                "coordinates": {
                    "row": 1,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 2,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 3,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " adsa",
                "confidence": 1.0,
                "coordinates": {
                    "row": 4,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " sdsa",
                "confidence": 1.0,
                "coordinates": {
                    "row": 5,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 6,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 0,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " ff",
                "confidence": 1.0,
                "coordinates": {
                    "row": 1,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " sda",
                "confidence": 1.0,
                "coordinates": {
                    "row": 2,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " C",
                "confidence": 1.0,
                "coordinates": {
                    "row": 3,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " Xaz",
                "confidence": 1.0,
                "coordinates": {
                    "row": 4,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 5,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " fdf",
                "confidence": 1.0,
                "coordinates": {
                    "row": 6,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 0,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 1,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 2,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " XC",
                "confidence": 1.0,
                "coordinates": {
                    "row": 3,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 4,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " |o#",
                "confidence": 1.0,
                "coordinates": {
                    "row": 5,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " 132",
                "confidence": 1.0,
                "coordinates": {
                    "row": 6,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " ewqsd",
                "confidence": 1.0,
                "coordinates": {
                    "row": 0,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 1,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " wee",
                "confidence": 1.0,
                "coordinates": {
                    "row": 2,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 3,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " ddsa",
                "confidence": 1.0,
                "coordinates": {
                    "row": 4,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 5,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
            {
                "value": " @#@#",
                "confidence": 1.0,
                "coordinates": {
                    "row": 6,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
            },
        ],
        "columns": [
            {"x": 0.0045894952},
            {"x": 0.2049974503},
            {"x": 0.402345742},
            {"x": 0.6042835288},
            {"x": 0.8021417644},
        ],
        "sourceId": "123",
        "coordinates": {
            "h": 0.13,
            "w": 0.7690196078431373,
            "x": 0.11725490196078431,
            "y": 0.10848484848484849,
        },
    }
]

tables_entities = [TableModel(**data).to_domain() for data in tables_data]

tables_data_with_table_bbox = [
    {
        "rows": [],
        "columns": [],
        "cells": [
            {
                "value": "ads",
                "confidence": 1.0,
                "coordinates": {
                    "row": 0,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.118039, "y": 0.109394, "w": 0.152941, "h": 0.018182}]}
                ],
            },
            {
                "value": "adsda",
                "confidence": 1.0,
                "coordinates": {
                    "row": 1,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.118039, "y": 0.127273, "w": 0.152941, "h": 0.017879}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 2,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.118039, "y": 0.144848, "w": 0.152941, "h": 0.017576}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 3,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.118039, "y": 0.162424, "w": 0.152941, "h": 0.017576}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 4,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.118039, "y": 0.18, "w": 0.152941, "h": 0.017576}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 5,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.118039, "y": 0.197879, "w": 0.152941, "h": 0.017879}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 6,
                    "page": 1,
                    "column": 0,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.118039, "y": 0.215455, "w": 0.152941, "h": 0.017576}]}
                ],
            },
            {
                "value": "13212",
                "confidence": 1.0,
                "coordinates": {
                    "row": 0,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.27098, "y": 0.109394, "w": 0.152549, "h": 0.017879}]}
                ],
            },
            {
                "value": "adsda",
                "confidence": 1.0,
                "coordinates": {
                    "row": 1,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.27098, "y": 0.127273, "w": 0.152549, "h": 0.017879}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 2,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.27098, "y": 0.144848, "w": 0.152549, "h": 0.017576}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 3,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.27098, "y": 0.162424, "w": 0.152549, "h": 0.017576}]}
                ],
            },
            {
                "value": "adsa",
                "confidence": 1.0,
                "coordinates": {
                    "row": 4,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.27098, "y": 0.18, "w": 0.152549, "h": 0.017576}]}
                ],
            },
            {
                "value": "sdsa",
                "confidence": 1.0,
                "coordinates": {
                    "row": 5,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.27098, "y": 0.197879, "w": 0.152549, "h": 0.017879}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 6,
                    "page": 1,
                    "column": 1,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.27098, "y": 0.215455, "w": 0.152549, "h": 0.017576}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 0,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.423529, "y": 0.109394, "w": 0.152941, "h": 0.017879}]}
                ],
            },
            {
                "value": "ff",
                "confidence": 1.0,
                "coordinates": {
                    "row": 1,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.423529, "y": 0.127273, "w": 0.152941, "h": 0.017576}]}
                ],
            },
            {
                "value": "sda",
                "confidence": 1.0,
                "coordinates": {
                    "row": 2,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.423529, "y": 0.144848, "w": 0.152941, "h": 0.017576}]}
                ],
            },
            {
                "value": "C",
                "confidence": 1.0,
                "coordinates": {
                    "row": 3,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.423529, "y": 0.162424, "w": 0.152941, "h": 0.017576}]}
                ],
            },
            {
                "value": "xaz",
                "confidence": 1.0,
                "coordinates": {
                    "row": 4,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.423529, "y": 0.18, "w": 0.152941, "h": 0.017576}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 5,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.423529, "y": 0.197879, "w": 0.152941, "h": 0.017879}]}
                ],
            },
            {
                "value": "fdf",
                "confidence": 1.0,
                "coordinates": {
                    "row": 6,
                    "page": 1,
                    "column": 2,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.423529, "y": 0.215455, "w": 0.152941, "h": 0.017576}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 0,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.576471, "y": 0.109394, "w": 0.152549, "h": 0.017879}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 1,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.576471, "y": 0.127273, "w": 0.152549, "h": 0.017879}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 2,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.576471, "y": 0.144848, "w": 0.152549, "h": 0.017576}]}
                ],
            },
            {
                "value": "xc",
                "confidence": 1.0,
                "coordinates": {
                    "row": 3,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.576471, "y": 0.162424, "w": 0.152549, "h": 0.017576}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 4,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.576471, "y": 0.18, "w": 0.152549, "h": 0.017576}]}
                ],
            },
            {
                "value": "!@#",
                "confidence": 1.0,
                "coordinates": {
                    "row": 5,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.576471, "y": 0.197879, "w": 0.152549, "h": 0.017576}]}
                ],
            },
            {
                "value": "132",
                "confidence": 1.0,
                "coordinates": {
                    "row": 6,
                    "page": 1,
                    "column": 3,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.576471, "y": 0.215455, "w": 0.152549, "h": 0.017576}]}
                ],
            },
            {
                "value": "ewqsd",
                "confidence": 1.0,
                "coordinates": {
                    "row": 0,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.72902, "y": 0.109394, "w": 0.153333, "h": 0.017879}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 1,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.72902, "y": 0.127273, "w": 0.153333, "h": 0.017576}]}
                ],
            },
            {
                "value": "wee",
                "confidence": 1.0,
                "coordinates": {
                    "row": 2,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.72902, "y": 0.144848, "w": 0.153333, "h": 0.017576}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 3,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.72902, "y": 0.162424, "w": 0.153333, "h": 0.017576}]}
                ],
            },
            {
                "value": "ddsa",
                "confidence": 1.0,
                "coordinates": {
                    "row": 4,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.72902, "y": 0.18, "w": 0.153333, "h": 0.017576}]}
                ],
            },
            {
                "value": "",
                "confidence": 1.0,
                "coordinates": {
                    "row": 5,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.72902, "y": 0.197879, "w": 0.153333, "h": 0.017879}]}
                ],
            },
            {
                "value": "!@#@#",
                "confidence": 1.0,
                "coordinates": {
                    "row": 6,
                    "page": 1,
                    "column": 4,
                    "colspan": 1,
                    "rowspan": 1,
                },
                "sourceBboxCoordinates": [
                    {"sourceId": "123", "bboxes": [{"x": 0.72902, "y": 0.215455, "w": 0.153333, "h": 0.017576}]}
                ],
            },
        ],
        "sourceBboxCoordinates": {"sourceId": "123", "bboxes": [{"x": 0.117647, "y": 0.109091, "w": 0.764706, "h": 0.142424}]},
    }
]

tables_with_bbox_entities = [TableModel(**data).to_domain() for data in tables_data_with_table_bbox]

textlines_for_table_with_bboxes = [
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="ads",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=301, y=361), right_bottom_point=PointEntity(x=691, y=420)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="adsda",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=301, y=420), right_bottom_point=PointEntity(x=691, y=478)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="13212",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=691, y=361), right_bottom_point=PointEntity(x=1080, y=420)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="adsda",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=691, y=420), right_bottom_point=PointEntity(x=1080, y=478)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="adsa",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=691, y=594), right_bottom_point=PointEntity(x=1080, y=653)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="sdsa",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=691, y=653), right_bottom_point=PointEntity(x=1080, y=711)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="ff",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1080, y=420), right_bottom_point=PointEntity(x=1470, y=478)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="sda",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1080, y=478), right_bottom_point=PointEntity(x=1470, y=536)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="C",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1080, y=536), right_bottom_point=PointEntity(x=1470, y=594)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="xaz",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1080, y=594), right_bottom_point=PointEntity(x=1470, y=653)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="fdf",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1080, y=711), right_bottom_point=PointEntity(x=1470, y=769)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="xc",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1470, y=536), right_bottom_point=PointEntity(x=1859, y=594)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="!@#",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1470, y=653), right_bottom_point=PointEntity(x=1859, y=711)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="132",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1470, y=711), right_bottom_point=PointEntity(x=1859, y=769)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="ewqsd",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1859, y=361), right_bottom_point=PointEntity(x=2250, y=420)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="wee",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1859, y=478), right_bottom_point=PointEntity(x=2250, y=536)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="ddsa",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1859, y=594), right_bottom_point=PointEntity(x=2250, y=653)),
            )
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="!@#@#",
                confidence=1.0,
                bbox=RectangleEntity(left_top_point=PointEntity(x=1859, y=711), right_bottom_point=PointEntity(x=2250, y=769)),
            )
        ],
    ),
]
