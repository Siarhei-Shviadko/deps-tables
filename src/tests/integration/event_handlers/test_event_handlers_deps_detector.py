import pytest
from pydantic import ValidationError

from deps_tables.events_handler.handlers import ocr_completed_handler
from tests.data import ocr_data, wrong_ocr_data


def test__ocr_completed_handler__deps_detector__no_errors(ocr_completed_envelope):
    ocr_completed_envelope.event.ocr_data = ocr_data
    ocr_completed_handler(ocr_completed_envelope)


def test__ocr_completed_handler__no_ocr_data__no_errors(ocr_completed_envelope):
    ocr_completed_envelope.event.ocr_data = []
    ocr_completed_handler(ocr_completed_envelope)


def test__ocr_completed_handler__wrong_ocr_data__validation_error(
    ocr_completed_envelope,
):
    ocr_completed_envelope.event.ocr_data = wrong_ocr_data
    with pytest.raises(ValidationError):
        ocr_completed_handler(ocr_completed_envelope)
