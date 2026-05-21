import numpy as np
from mock import Mock


class TestIdentifierService:
    def test_is_table_on_page(self, table_identifier_service):
        page = np.zeros((10, 10), dtype=np.uint8)

        table_identifier_service.table_identifier = Mock()

        table_identifier_service.enabled = False
        assert table_identifier_service.is_table_on_page(page) is True

        table_identifier_service.enabled = True

        table_identifier_service.table_identifier.is_table_on_image.return_value = False
        assert table_identifier_service.is_table_on_page(page) is False
        table_identifier_service.table_identifier.is_table_on_image.assert_called_with(page)

        table_identifier_service.table_identifier.is_table_on_image.return_value = True
        assert table_identifier_service.is_table_on_page(page) is True
        table_identifier_service.table_identifier.is_table_on_image.assert_called_with(page)

    def test_identify_table_borders(self, table_identifier_service):
        tis = table_identifier_service

        page = np.zeros((10, 10), dtype=np.uint8)

        tis.table_identifier = Mock()

        tis.enabled = False
        assert tis.identify_table_borders(page) == []

        tis.enabled = True
        box = "Box"
        tis.table_identifier.identify_borders.return_value = [box]
        expected = [box]
        actual = tis.identify_table_borders(page)
        assert actual == expected
        tis.table_identifier.identify_borders.assert_called_with(page)
