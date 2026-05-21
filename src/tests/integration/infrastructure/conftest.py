import pytest


@pytest.fixture(scope="module", autouse=True)
def existing_file(storage):
    with open("tests/data/table.png", "rb") as f:
        storage._upload_file("some_dir/some_subdir", "table.png", f)
