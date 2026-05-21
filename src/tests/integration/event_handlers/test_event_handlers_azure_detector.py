from unittest import mock

import pytest
from azure.ai.formrecognizer import DocumentAnalysisClient
from pydantic import ValidationError

from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.events_handler.handlers import ocr_completed_handler
from deps_tables.infrastructure.table_extractors.azure_table_extractor import (
    AzureTableAdapter,
)
from tests.data import ocr_data, wrong_ocr_data
from tests.data.tables_data import tables_entities


@pytest.fixture
def azure_client_mock():
    content = mock.Mock()
    content.result.return_value = []
    patcher = mock.patch.object(DocumentAnalysisClient, "begin_analyze_document", return_value=content)
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture
def azure_table_adapter_mock():
    patcher = mock.patch.object(AzureTableAdapter, "convert_to_domain_table", return_value=tables_entities)
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture
def enabled_azure_detector_mock(settings, azure_client_mock, azure_table_adapter_mock):
    settings["enabled_detectors"].append(TableDetectionEngineEnum.AZURE_FORM_RECOGNIZER)
    yield
    settings["enabled_detectors"].remove(TableDetectionEngineEnum.AZURE_FORM_RECOGNIZER)


def test__ocr_completed_handler__azure_detector__no_errors(ocr_completed_envelope, enabled_azure_detector_mock):
    ocr_completed_envelope.event.ocr_data = ocr_data
    ocr_completed_envelope.event.extraction_params["table_detection_engine"] = TableDetectionEngineEnum.AZURE_FORM_RECOGNIZER
    ocr_completed_handler(ocr_completed_envelope)


def test__ocr_completed_handler__wrong_ocr_data__validation_error(ocr_completed_envelope, enabled_azure_detector_mock):
    ocr_completed_envelope.event.ocr_data = wrong_ocr_data
    with pytest.raises(ValidationError):
        ocr_completed_handler(ocr_completed_envelope)
