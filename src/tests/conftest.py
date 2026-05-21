import os
from io import BytesIO

import pytest
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)
from fastapi.testclient import TestClient
from pytest_factoryboy import register

from deps_tables.api_app import create_app
from deps_tables.extras.services import StorageControllerService
from deps_tables.extras.services.exceptions import FileStorageRequestError
from deps_tables.infrastructure.access_management.context_vars import user
from tests.factories import TableFactory

PRIVILEGED_GROUP: str = "deps-admins"


@pytest.fixture(scope="module", autouse=False)
def fastapi_app():
    app = create_app()

    yield app


@pytest.fixture(scope="module", autouse=False)
def application(fastapi_app):
    yield fastapi_app.app


@pytest.fixture
def services(application):
    application.reset_singletons()
    yield application.services
    application.reset_singletons()


@pytest.fixture(scope="module", autouse=True)
def settings(application):
    config = application.config()
    config["preinit_detectors"] = False
    config["enable_gpu"] = False

    yield config


@pytest.fixture(scope="module", autouse=False)
def client(fastapi_app):
    return TestClient(fastapi_app)


@pytest.fixture(scope="module", autouse=True)
def storage(application):
    storage = MockedFileStorage()
    application.external_services.storage_controller_service.override(storage)

    yield storage


@pytest.fixture(scope="session")
def test_image_file_content():
    image_path = "tests/data/test_tables_0.jpg"
    image_file = open(image_path, "rb")
    content = image_file.read()
    yield content


@pytest.fixture(scope="function")
def test_image_file(test_image_file_content):
    yield BytesIO(test_image_file_content)


class MockedFileStorage(StorageControllerService):
    def __init__(self):
        self.storage_dict = {}
        self._storage = "FILE_STORAGE"

    def download_content(self, file_path, storage="FILE_STORAGE"):
        if file_path not in self.storage_dict:
            raise FileStorageRequestError(f"File with path {file_path} is not found.")
        return self.storage_dict[file_path]

    def delete_file(self, file_path, storage="FILE_STORAGE"):
        if file_path in self.storage_dict:
            del self.storage_dict[file_path]

    def _upload_file(
        self,
        file_path,
        filename,
        file_object,
        storage="FILE_STORAGE",
        replace_if_exists=False,
    ):
        file_path = os.path.join(file_path, filename)
        if not replace_if_exists and file_path in self.storage_dict:
            raise FileStorageRequestError(f"File with path {file_path} already exists.")
        self.storage_dict[file_path] = file_object.read()

        return file_path


@pytest.fixture
def ocr_completed_envelope(mocker):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.document_id = 123
    dee.event.source_id = "123"
    dee.event.file_path = "some_dir/some_subdir/table.png"
    dee.event.extraction_params = {"tables": True}
    dee.event.identify_document = False
    dee.event.extract_data = False
    dee.event.document_type = None
    return dee


@pytest.fixture
def regular_user():
    return {
        "subject": "regular",
        "roles": [],
        "groups": ["deps-users"],
        "token": "token",
        "email": "example@mail.com",
        "first_name": "John",
        "last_name": "Doe",
        "organisation": "deps-users",
    }


@pytest.fixture
def privileged_user():
    return {
        "subject": "privileded",
        "roles": [],
        "groups": [PRIVILEGED_GROUP],
        "token": "token",
        "email": "example@mail.com",
        "first_name": "John",
        "last_name": "Doe",
        "organisation": PRIVILEGED_GROUP,
    }


@pytest.fixture
def set_regular_user(regular_user):
    token = user.set(regular_user)
    yield
    user.reset(token)


@pytest.fixture
def set_privileged_user(privileged_user):
    token = user.set(privileged_user)
    yield
    user.reset(token)


register(TableFactory)


@pytest.fixture
def enable_paid_engine_restriction(application):
    with application.config.paid_engines_restriction_enabled.override(True):
        with application.config.privileged_group.override(PRIVILEGED_GROUP):
            yield
