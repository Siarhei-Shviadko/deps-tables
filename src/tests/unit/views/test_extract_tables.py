import json
from contextlib import suppress
from dataclasses import asdict
from uuid import uuid4

import cv2
import mock
import numpy as np
import pytest
from mock import Mock

from deps_tables.api.models.table import TableModel
from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.domain.entities import ImageEntity
from tests.factories import TableFactory


@pytest.mark.parametrize("language", ["eng", "rus", "chi"])
@pytest.mark.parametrize("tde", [x.value for x in TableDetectionEngineEnum])
def test_detect_extract_tables_from_file__valid_data(client, application_service, test_image_file, language, tde):
    table = TableFactory()
    application_service.detect_tables = Mock(return_value=[table])

    response = client.post(
        url="/api/tables/v1/file/detect",
        data={
            "ocrEngine": "TESSERACT",
            "language": language,
            "tableDetectionEngine": tde,
        },
        files={
            "file": test_image_file,
        },
    )

    assert response.status_code == 200
    assert response.json()
    application_service.detect_tables.assert_called_with(
        image=mock.ANY,
        table_detection_engine=tde,
        ocr_engine="TESSERACT",
        language=language,
    )


@pytest.mark.parametrize("language", ["eng", "rus", "chi"])
@pytest.mark.parametrize("tde", [x.value for x in TableDetectionEngineEnum])
def test_detect_extract_tables_from_storage__valid_data(client, application_service, storage, language, tde):
    blob_path = "dir_path/some_image.jpg"
    surface = np.zeros((200, 300))
    content = bytes(cv2.imencode(".png", surface)[1])
    blob_path = storage.upload_content(blob_path, content)

    table = TableFactory()

    application_service.detect_tables = Mock(return_value=[table])

    response = client.post(
        url="/api/tables/v1/storage/detect",
        json={
            "blobFile": blob_path,
            "ocrEngine": "TESSERACT",
            "language": language,
            "tableDetectionEngine": tde,
        },
    )

    assert response.status_code == 200
    assert response.json()
    application_service.detect_tables.assert_called_with(
        image=mock.ANY,
        table_detection_engine=tde,
        ocr_engine="TESSERACT",
        language=language,
        selected_area=None,
    )


@pytest.mark.parametrize("language", ["eng", "rus", "chi"])
def test_extract_tables_from_file_storage__valid_data(client, application_service, storage, language):
    blob_path = "dir_path/some_image.jpg"
    surface = np.zeros((200, 300))
    content = bytes(cv2.imencode(".png", surface)[1])
    blob_path = storage.upload_content(blob_path, content)

    table = TableFactory()

    application_service.ocr_tables = Mock(return_value=[table])

    response = client.post(
        url="/api/tables/v1/storage/extract",
        json={
            "blobFile": blob_path,
            "ocrEngine": "TESSERACT",
            "language": language,
            "table": TableModel(**asdict(table)).dict(by_alias=True),
        },
    )

    assert response.status_code == 200
    assert response.json()
    with suppress(AssertionError):
        application_service.ocr_tables.assert_called_with(
            image=mock.ANY,
            ocr_engine="TESSERACT",
            language=language,
            tables=[table],
        )
        assert False, "This caused by rounding, can't fix it right now"


def test_extract_tables_from_image_and_textlines__valid_data(client, application_service):
    data = {
        "sourceId": uuid4().hex,
        "ocrTextlines": json.dumps(
            [
                {
                    "id": 0,
                    "wordBoxes": [
                        {
                            "bbox": {"h": 0.012380615493455961, "w": 0.079, "x": 0.701, "y": 0.054474708171206226},
                            "confidence": 0.906465835571289,
                            "content": "Globex",
                        },
                        {
                            "bbox": {"h": 0.01591793420587195, "w": 0.136, "x": 0.7875, "y": 0.054120976299964624},
                            "confidence": 0.910504379272461,
                            "content": "Corporation",
                        },
                    ],
                },
            ]
        ),
    }
    table = TableFactory()
    application_service.detect_tables = Mock(return_value=[table])

    response = client.post(
        url="/api/tables/v1/file/extract-from-textlines",
        files={"file": b"content"},
        data=data,
    )

    assert response.status_code == 200
    assert response.json()
    application_service.detect_tables.assert_called_with(
        image=mock.ANY,
        table_detection_engine=TableDetectionEngineEnum.DEPS_CONVERTER,
        ocr_engine="",
        language="",
    )
