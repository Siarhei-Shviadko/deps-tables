from unittest import mock

import pytest
from google.cloud import documentai
from google.oauth2.service_account import Credentials
from pydantic import ValidationError

from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.events_handler.handlers import ocr_completed_handler
from deps_tables.infrastructure.table_extractors.gcp_table_extractor import (
    GCPTableAdapter,
)
from tests.data import ocr_data, wrong_ocr_data
from tests.data.tables_data import tables_entities


@pytest.fixture
def gcp_credentials_mock():
    content = mock.Mock()
    patcher = mock.patch.object(Credentials, "from_service_account_info", return_value=content)
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture
def gcp_client_mock():
    content = mock.Mock()
    content.result.return_value = []
    patcher = mock.patch.object(documentai.DocumentProcessorServiceClient, "process_document", return_value=content)
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture
def gcp_table_adapter_mock():
    patcher = mock.patch.object(GCPTableAdapter, "convert_to_domain_table", return_value=tables_entities)
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture
def enabled_gcp_detector_mock(settings, gcp_client_mock, gcp_table_adapter_mock, gcp_credentials_mock):
    settings["enabled_detectors"].append(TableDetectionEngineEnum.GCP_FORM_PARSER)
    yield
    settings["enabled_detectors"].remove(TableDetectionEngineEnum.GCP_FORM_PARSER)


def test__ocr_completed_handler__gcp_detector__no_errors(ocr_completed_envelope, enabled_gcp_detector_mock):
    ocr_completed_envelope.event.ocr_data = ocr_data
    ocr_completed_envelope.event.extraction_params["table_detection_engine"] = TableDetectionEngineEnum.GCP_FORM_PARSER
    ocr_completed_handler(ocr_completed_envelope)


def test__ocr_completed_handler__wrong_ocr_data__validation_error(ocr_completed_envelope, enabled_gcp_detector_mock):
    ocr_completed_envelope.event.ocr_data = wrong_ocr_data
    with pytest.raises(ValidationError):
        ocr_completed_handler(ocr_completed_envelope)
