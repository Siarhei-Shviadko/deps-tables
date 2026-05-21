from http import HTTPStatus
from unittest.mock import patch

import pytest

from deps_tables.api.constants import DETECTION_ENGINE_NAMES
from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.infrastructure.table_extractors.deps_table_extractor import (
    DepsTablesExtractor,
)
from tests.factories import TableFactory


@pytest.fixture
def set_detection_engines(services):
    old_value = services.config.enabled_detectors()
    services.config.set("enabled_detectors", [TableDetectionEngineEnum.DEPS_DETECTOR])
    yield
    services.config.set("enabled_detectors", old_value)


EXPECTED_RESULT = [
    {
        "code": TableDetectionEngineEnum.DEPS_DETECTOR.value,
        "name": DETECTION_ENGINE_NAMES[TableDetectionEngineEnum.DEPS_DETECTOR],
    }
]


@pytest.mark.usefixtures("set_detection_engines")
class TestGetAvailableEngines:
    endpoint = "/api/tables/v1/detection-engines"

    def test_get_available_engines__success(self, client):
        response = client.get(self.endpoint)
        data = response.json()

        assert response.status_code == HTTPStatus.OK
        assert data == EXPECTED_RESULT


class TestExtractTables:
    endpoint = "/api/tables/v1/file/detect"

    def test_extract_tables__engine_is_available__success(self, client, test_image_file):
        with patch.object(DepsTablesExtractor, "extract_tables", return_value=[TableFactory()]):
            response = client.post(
                url=self.endpoint,
                data={
                    "tableDetectionEngine": TableDetectionEngineEnum.DEPS_DETECTOR.value,
                },
                files={
                    "file": test_image_file,
                },
            )

        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) == 1

    @pytest.mark.parametrize(
        "disabled_detector",
        [
            TableDetectionEngineEnum.AWS_TEXTRACT,
            TableDetectionEngineEnum.AZURE_FORM_RECOGNIZER,
        ],
    )
    def test_extract_tables__engine_is_not_available__404(self, client, test_image_file, disabled_detector):
        with patch.object(DepsTablesExtractor, "extract_tables", return_value=[TableFactory()]):
            response = client.post(
                url=self.endpoint,
                data={
                    "tableDetectionEngine": disabled_detector.value,
                },
                files={
                    "file": test_image_file,
                },
            )

        assert response.status_code == HTTPStatus.NOT_FOUND
