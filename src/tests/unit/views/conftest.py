import pytest


@pytest.fixture(scope="module", autouse=False)
def application_service(application):
    yield application.application()
