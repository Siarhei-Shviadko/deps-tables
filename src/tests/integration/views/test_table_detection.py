from http import HTTPStatus

import cv2
import numpy as np
import pytest

from deps_tables.domain.entities import RelativeAreaEntityWithPage
from tests.factories import TableFactory


@pytest.fixture
def empty_image():
    w, h = 1000, 1000
    image = np.zeros((h, w, 3), dtype=np.uint8)

    return image


def convert_image_to_content(image) -> str:
    content = cv2.imencode(".png", image)[1].tostring()

    return content


class TestAPIStorageDetectTables:
    endpoint = "/api/tables/v1/storage/detect"

    def test_detect_tables_from_storage__without_area(self, client, tds_mock, storage, empty_image):
        blob_name = "blob_name"
        tds_mock.execute.return_value = [
            TableFactory(
                coordinates=RelativeAreaEntityWithPage(
                    left=0.101,
                    top=0.102,
                    width=0.103,
                    height=0.104,
                )
            )
        ]
        storage.storage_dict[blob_name] = convert_image_to_content(empty_image)

        response = client.post(
            url=self.endpoint,
            json={
                "blobFile": blob_name,
            },
        )
        data = response.json()

        expected_coordinates = {
            "x": 0.101,
            "y": 0.102,
            "w": 0.103,
            "h": 0.104,
            "page": 1,
        }

        assert response.status_code == HTTPStatus.OK
        assert data[0]["coordinates"] == expected_coordinates

    def test_detect_tables_from_storage__with_area(self, client, tds_mock, storage, empty_image):
        blob_name = "blob_name"
        tds_mock.execute.return_value = [
            TableFactory(
                coordinates=RelativeAreaEntityWithPage(
                    left=0.2525,
                    top=0.255,
                    width=0.53,
                    height=0.54,
                )
            )
        ]
        storage.storage_dict[blob_name] = convert_image_to_content(empty_image)

        response = client.post(
            url=self.endpoint,
            json={
                "blobFile": blob_name,
                "area": {
                    "x": 0.1,
                    "y": 0.2,
                    "w": 0.4,
                    "h": 0.4,
                },
            },
        )
        data = response.json()
        for k, v in data[0]["coordinates"].items():
            data[0]["coordinates"][k] = round(v, 6)

        expected_coordinates = {
            "x": 0.201,
            "y": 0.302,
            "w": 0.212,
            "h": 0.216,
            "page": 1,
        }

        assert response.status_code == HTTPStatus.OK
        assert data[0]["coordinates"] == expected_coordinates
