import numpy as np
import pytest

from deps_tables.domain.entities import ImageEntity
from deps_tables.extras.auth.deps_auth import AUTH_HEADER, JWT_PREFIX
from deps_tables.infrastructure.access_management.context_vars import (
    user as user_context_var,
)


@pytest.fixture(scope="function")
def image():
    surface = np.zeros((100, 100))
    return ImageEntity(image=surface)


@pytest.fixture
def user_fixture():
    return {
        "subject": "some_user_id",
        "roles": [],
        "groups": ["deps-users"],
        "token": "token",
    }


@pytest.fixture
def set_test_user(user_fixture):
    user_context_var.set(user_fixture)


@pytest.fixture
def enable_authorization_for_external_services(application):
    application.external_services.config.authentication.enabled.override(True)
    yield
    application.external_services.config.authentication.enabled.override(False)


@pytest.mark.usefixtures("enable_authorization_for_external_services", "set_test_user")
def test_extraction__auth_enabled__auth_token_is_set(ocr_service, application, settings, user_fixture, image, requests_mock):
    requests_mock.post(settings["ocr_api_url"], status_code=200, json=[])
    application.external_services.ocr_controller_service().set_user_context(user_context_var)
    ocr_service.extract_data(image_obj=image, engine="TESSERACT")

    request_headers = requests_mock.request_history[0].headers
    assert request_headers[AUTH_HEADER] == f"{JWT_PREFIX}{user_fixture['token']}"


def test_extraction__auth_disabled__auth_token_is_empty(ocr_service, application, settings, image, requests_mock):
    requests_mock.post(settings["ocr_api_url"], status_code=200, json=[])
    ocr_service.extract_data(image_obj=image, engine="TESSERACT")

    request_headers = requests_mock.request_history[0].headers
    assert AUTH_HEADER not in request_headers
