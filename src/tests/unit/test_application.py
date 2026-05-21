import numpy as np
import pytest
from mock import Mock

from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.domain.entities import ImageEntity
from tests.factories import TableFactory


class TestApplicationService:
    @pytest.mark.parametrize("language", ["eng", "rus", "chi"])
    def test_extract_tables_from_image__valid_data(self, application_service, language):
        image = ImageEntity(
            image=np.zeros((10, 10)),
            blob_path=None,
            meta=None,
        )
        expected_table = TableFactory()
        expected_tables = [expected_table]
        application_service._ocr_table_service.extract_data_from_table.return_value = expected_table

        tables = application_service.ocr_tables(
            image=image,
            ocr_engine="TESSERACT",
            language=language,
            tables=expected_tables,
        )

        application_service._ocr_table_service.extract_data_from_table.assert_called_with(
            image, expected_table, engine="TESSERACT", language=language
        )
        assert tables == expected_tables

    @pytest.mark.parametrize("table_detection_engine", [x for x in TableDetectionEngineEnum])
    def test_get_detected_tables__valid_data(self, application_service, table_detection_engine):
        image = ImageEntity(
            image=np.zeros((10, 10)),
            blob_path=None,
            meta=None,
        )
        expected_tables = [TableFactory()]
        application_service._table_extraction_service.execute = Mock(return_value=expected_tables)

        tables = application_service.detect_tables(
            image=image,
            table_detection_engine=table_detection_engine,
            ocr_engine="TESSERACT",
            language="eng",
        )

        application_service._table_extraction_service.execute.assert_called_with(
            image=image,
            detector=table_detection_engine,
            ocr_engine="TESSERACT",
            language="eng",
        )
        assert tables == expected_tables
