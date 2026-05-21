import io
from http import HTTPStatus

import cv2
import numpy as np
import pytest

from deps_tables.api.constants import FREE_DETECTION_ENGINES
from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.infrastructure.access_management.context_vars import user


@pytest.fixture
def mock_application(application, mocker):
    mock = mocker.Mock(application.application.cls)
    with application.application.override(mock):
        yield mock


@pytest.fixture
def enabled_detectors():
    return [
        TableDetectionEngineEnum.DEPS_DETECTOR,
        TableDetectionEngineEnum.AWS_TEXTRACT,
        TableDetectionEngineEnum.AZURE_FORM_RECOGNIZER,
    ]


@pytest.fixture
def free_detectors():
    return FREE_DETECTION_ENGINES


@pytest.fixture
def paid_detectors():
    return [
        TableDetectionEngineEnum.AWS_TEXTRACT,
        TableDetectionEngineEnum.AZURE_FORM_RECOGNIZER,
    ]


@pytest.fixture(autouse=True)
def set_enabled_detectors(application, enabled_detectors, enable_paid_engine_restriction):
    with application.config.enabled_detectors.override(enabled_detectors):
        yield


@pytest.fixture
def uploaded_file(storage):
    surface = np.zeros((10, 10))
    content = bytes(cv2.imencode(".png", surface)[1])
    blob_path = storage.upload_content("dir_path/some_image.jpg", content)
    return blob_path


class TestGetAvailableDetectors:
    endpoint = "/api/tables/v1/detection-engines"

    def test_get_available_detectors__regular_user__only_free_detectors(self, regular_user, client):
        expected_result = [{"code": "DEPS_DETECTOR", "name": "DEPS Detector"}]
        user.set(regular_user)

        response = client.get(self.endpoint)
        data = response.json()

        assert response.status_code == HTTPStatus.OK
        assert data == expected_result

    def test_get_available_detectors__privileged_user__enabled_detectors(self, privileged_user, client):
        expected_result = [
            {"code": "DEPS_DETECTOR", "name": "DEPS Detector"},
            {"code": "AWS_TEXTRACT", "name": "Amazon Textract"},
            {"code": "AZURE_FORM_RECOGNIZER", "name": "Azure Form Recognizer"},
        ]
        user.set(privileged_user)

        response = client.get(self.endpoint)
        data = response.json()

        assert response.status_code == HTTPStatus.OK
        assert data == expected_result


class TestExtractTablesFromFile:
    endpoint = "/api/tables/v1/file/detect"

    def test_extract_table__regular_user__free_detectors__success(self, client, free_detectors, regular_user, mock_application):
        mock_application.detect_tables.return_value = []
        user.set(regular_user)

        for detector in free_detectors:
            response = client.post(
                self.endpoint,
                data={"tableDetectionEngine": detector.value},
                files={"file": ("test.png", io.BytesIO(b"image"))},
            )

            assert response.status_code == HTTPStatus.OK
            assert response.json() == []

    def test_extract_table__privileged_user__enabled_detectors__success(
        self, client, enabled_detectors, privileged_user, mock_application
    ):
        mock_application.detect_tables.return_value = []
        user.set(privileged_user)

        for detector in enabled_detectors:
            response = client.post(
                self.endpoint,
                data={"tableDetectionEngine": detector.value},
                files={"file": ("test.png", io.BytesIO(b"image"))},
            )

            assert response.status_code == HTTPStatus.OK
            assert response.json() == []

    def test_extract_table__regular_user__paid_detectors__forbidden(self, client, paid_detectors, regular_user, mock_application):
        mock_application.detect_tables.return_value = []
        user.set(regular_user)

        for detector in paid_detectors:
            response = client.post(
                self.endpoint,
                data={"tableDetectionEngine": detector.value},
                files={"file": ("test.png", io.BytesIO(b"image"))},
            )

            assert response.status_code == HTTPStatus.FORBIDDEN


class TestDetectTablesFromFileStorage:
    endpoint = "/api/tables/v1/storage/detect"

    def test_detect_table__regular_user__free_detectors__success(
        self, client, free_detectors, regular_user, mock_application, uploaded_file
    ):
        mock_application.detect_tables.return_value = []
        user.set(regular_user)

        for detector in free_detectors:
            response = client.post(
                self.endpoint,
                json={
                    "tableDetectionEngine": detector.value,
                    "blobFile": uploaded_file,
                },
            )

            assert response.status_code == HTTPStatus.OK
            assert response.json() == []

    def test_detect_table__privileged_user__enabled_detectors__success(
        self, client, enabled_detectors, privileged_user, mock_application, uploaded_file
    ):
        mock_application.detect_tables.return_value = []
        user.set(privileged_user)

        for detector in enabled_detectors:
            response = client.post(
                self.endpoint,
                json={
                    "tableDetectionEngine": detector.value,
                    "blobFile": uploaded_file,
                },
            )

            assert response.status_code == HTTPStatus.OK
            assert response.json() == []

    def test_detect_table__regular_user__paid_detectors__forbidden(
        self, client, paid_detectors, regular_user, mock_application, uploaded_file
    ):
        mock_application.detect_tables.return_value = []
        user.set(regular_user)

        for detector in paid_detectors:
            response = client.post(
                self.endpoint,
                json={
                    "tableDetectionEngine": detector.value,
                    "blobFile": uploaded_file,
                },
            )

            assert response.status_code == HTTPStatus.FORBIDDEN
