import pytest

from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.domain.exceptions import ForbiddenError
from deps_tables.events_handler.handlers import ocr_completed_handler
from tests.data import ocr_data


@pytest.fixture
def enable_aws_gcp_detectors(application):
    with application.config.enabled_detectors.override(
        [TableDetectionEngineEnum.AWS_TEXTRACT, TableDetectionEngineEnum.GCP_FORM_PARSER],
    ):
        yield


@pytest.mark.parametrize("ocr_engine", ["AWS_TEXTRACT", "GCP_VISION"])
def test__ocr_completed_handler__regular_user__error(
    enable_paid_engine_restriction,
    enable_aws_gcp_detectors,
    ocr_completed_envelope,
    set_regular_user,
    ocr_engine,
):
    ocr_completed_envelope.event.ocr_data = ocr_data
    ocr_completed_envelope.event.extraction_params["ocr_engine"] = ocr_engine
    with pytest.raises(ForbiddenError):
        ocr_completed_handler(ocr_completed_envelope)
