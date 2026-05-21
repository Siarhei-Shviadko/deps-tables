import numpy as np
import pytest

from deps_tables.infrastructure.heuristic.rows_detection import RowsIdentifier


class TestRowDetection:
    @pytest.mark.skip
    def test_rows_correction(self):
        pass

    @pytest.mark.skip
    def test_easy_rows_correction(self):
        pass

    def test_intersec_row_box(self):
        rows = [20, 60, 110]
        expected_intersec_row_box = [[], [], [125, 142]]
        boxes = [
            [20, 200, 200, 240],
            [35, 180, 125, 220],
            [150, 230, 160, 210],
            [190, 180, 210, 210],
            [160, 155, 180, 185],
            [40, 70, 90, 125],
            [60, 100, 110, 142],
            [130, 110, 170, 140],
        ]
        res = []
        for row in rows:
            kek = RowsIdentifier()._intersec_row_box(row, boxes)
            res.append(kek)
        assert res == expected_intersec_row_box

    @pytest.mark.skip
    def test_rows_identification(self):
        pass

    @pytest.mark.skip
    def test_identify_borders(self):
        pass
