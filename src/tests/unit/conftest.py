import pytest
from mock import Mock

from deps_tables.application import ApplicationService
from deps_tables.domain.entities.table_detector import TableDetectorInitSettings
from deps_tables.domain.services import (
    OCRTableService,
    TableExtractionService,
    TableIdentifierService,
)
from deps_tables.infrastructure.bbox_identifiers import TableBorderIdentifier
from deps_tables.infrastructure.services import OCRDataConverter, OCRService


@pytest.fixture
def valid_decoded_token():
    return {"groups": ["Test group"]}


@pytest.fixture(params=[[], ["Test group 1", "Test group 2"]])
def invalid_decoded_token(request):
    return {"groups": request.param}


@pytest.fixture(scope="function", autouse=False)
def ocr_service(settings):
    yield OCRService(
        ocr_settings=settings,
        ocr_service=Mock(),
    )


@pytest.fixture
def ocr_converter():
    yield OCRDataConverter()


@pytest.fixture(scope="function", autouse=False)
def table_identifier_service(settings):
    # Should be enabled at the start of tests if you are going to test the real identification
    yield TableIdentifierService(
        table_identifier_cls=TableDetectorInitSettings(
            detector_cls=TableBorderIdentifier,
            detector_args=(
                settings["table_identifier_model_weights_path"],
                settings["enable_gpu"],
            ),
        ),
        enable_table_identifier=False,
    )


@pytest.fixture(scope="function", autouse=False)
def ocr_table_service():
    yield OCRTableService(
        ocr_service=Mock(),
    )


@pytest.fixture(scope="function", autouse=False)
def table_detection_service(table_identifier_service):
    yield TableExtractionService(
        preinit_detectors=False,
        registered_detectors={},
        table_identifier=table_identifier_service,
    )


@pytest.fixture(scope="function", autouse=False)
def application_service():
    yield ApplicationService(
        table_extraction_service=Mock(),
        ocr_table_service=Mock(),
    )


@pytest.fixture(scope="function", autouse=False)
def ocr_table_service_with_ocr_service(settings):
    yield OCRTableService(
        ocr_service=OCRService(
            ocr_settings=settings,
            ocr_service=Mock(),
        )
    )
