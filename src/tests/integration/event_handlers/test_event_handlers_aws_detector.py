from unittest import mock

import boto3
import pytest
from pydantic import ValidationError

from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.events_handler.handlers import ocr_completed_handler
from deps_tables.infrastructure.table_extractors.aws_table_extractor import (
    AWSTableAdapter,
)
from tests.data import ocr_data, wrong_ocr_data
from tests.data.tables_data import tables_entities


@pytest.fixture
def boto3_client_mock():
    client_mock = mock.Mock()
    client_mock.analyze_document.return_value = []
    patcher = mock.patch.object(boto3, "client", new_callable=mock.PropertyMock(return_value=client_mock))
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture
def aws_table_adapter_mock():
    patcher = mock.patch.object(AWSTableAdapter, "convert_to_domain_table", return_value=tables_entities)
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture
def aws_detector_mock(settings, boto3_client_mock, aws_table_adapter_mock):
    settings["enabled_detectors"].append(TableDetectionEngineEnum.AWS_TEXTRACT)
    yield
    settings["enabled_detectors"].remove(TableDetectionEngineEnum.AWS_TEXTRACT)


def test__ocr_completed_handler__aws_detector__no_errors(ocr_completed_envelope, aws_detector_mock):
    ocr_completed_envelope.event.ocr_data = ocr_data
    ocr_completed_envelope.event.extraction_params["table_detection_engine"] = TableDetectionEngineEnum.AWS_TEXTRACT
    ocr_completed_handler(ocr_completed_envelope)


def test__ocr_completed_handler__wrong_ocr_data__validation_error(ocr_completed_envelope, aws_detector_mock):
    ocr_completed_envelope.event.ocr_data = wrong_ocr_data
    with pytest.raises(ValidationError):
        ocr_completed_handler(ocr_completed_envelope)
