import pytest

from deps_tables import Settings
from deps_tables.api_app import create_app


@pytest.fixture(scope="module")
def fastapi_app():
    config = Settings()
    config.ocr_version = "converter"
    app = create_app(config)

    yield app


@pytest.fixture(scope="module", autouse=True)
def existing_file(storage):
    with open("tests/data/table.png", "rb") as f:
        storage._upload_file("some_dir/some_subdir", "table.png", f)
