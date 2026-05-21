from deps_tables.infrastructure.heuristic import utils as util
from deps_tables.infrastructure.heuristic.columns_detection import ColumnsCorrection

columns = [
    [0, 12, 629, 2402],
    [1787, 2, 2190, 2399],
    [1205, 228, 1767, 2402],
    [833, 152, 1176, 2396],
    [653, 48, 816, 2402],
]
expected_sorted_columns = [
    [0, 12, 629, 2402],
    [653, 48, 816, 2402],
    [833, 152, 1176, 2396],
    [1205, 228, 1767, 2402],
    [1787, 2, 2190, 2399],
]
expected_fixed_columns = [
    [300, 200, 700, 2050],
    [800, 120, 1400, 2050],
    [1600, 100, 2000, 2060],
    [1900, 90, 2200, 2070],
]
columns_to_sort = [
    [190, 310, 250, 380],
    [260, 340, 300, 410],
    [10, 10, 150, 200],
    [170, 210, 230, 280],
    [290, 220, 450, 300],
    [10, 330, 170, 400],
    [310, 330, 379, 390],
    [160, 10, 250, 200],
    [270, 10, 370, 200],
    [10, 220, 150, 300],
]
for_contraction = [
    [(10, 10, 150, 200), (160, 10, 250, 200), (270, 10, 370, 200), (290, 10, 450, 200)],
    [(130, 210, 250, 300), (10, 210, 150, 300)],
    [
        (390, 310, 450, 400),
        (410, 310, 500, 400),
        (530, 310, 600, 400),
        (10, 310, 150, 400),
        (160, 310, 250, 400),
        (230, 310, 300, 400),
        (280, 310, 370, 400),
    ],
]
excepted_columns_contraction = [
    (10, 10, 150, 200),
    (160, 10, 250, 200),
    (270, 10, 329, 200),
    (331, 10, 450, 200),
    (10, 210, 139, 300),
    (141, 210, 250, 300),
    (10, 310, 150, 400),
    (160, 310, 239, 400),
    (241, 310, 289, 400),
    (291, 310, 370, 400),
    (390, 310, 429, 400),
    (431, 310, 500, 400),
    (530, 310, 600, 400),
]
lines_from_columns = [
    [10, 10, 150, 200],
    [160, 10, 250, 200],
    [270, 10, 370, 200],
    [290, 220, 450, 300],
    [10, 220, 150, 300],
    [170, 210, 230, 280],
    [10, 330, 170, 400],
    [190, 310, 250, 380],
    [260, 340, 300, 410],
    [310, 330, 379, 390],
]
res_for_lines_from_columns = [
    [[10, 10, 150, 200], [160, 10, 250, 200], [270, 10, 370, 200]],
    [[290, 220, 450, 300], [10, 220, 150, 300], [170, 210, 230, 280]],
    [
        [10, 330, 170, 400],
        [190, 310, 250, 380],
        [260, 340, 300, 410],
        [310, 330, 379, 390],
    ],
]
sorted_lines = [
    [[10, 10, 150, 200], [160, 10, 250, 200], [270, 10, 370, 200]],
    [[10, 220, 150, 300], [170, 210, 230, 280], [290, 220, 450, 300]],
    [
        [10, 330, 170, 400],
        [190, 310, 250, 380],
        [260, 340, 300, 410],
        [310, 330, 379, 390],
    ],
]
MERGE_COLUMNS_THRESHOLD = 0.7


class TestColumnDetection:
    def test_sort_columns(self):
        result = ColumnsCorrection().sort_columns(columns_to_sort)
        assert result == sorted_lines

    def test_column_contraction(self):
        res_columns = []
        for column_line in for_contraction:
            res_columns.extend(ColumnsCorrection().contract_column(sorted(column_line, key=lambda x: x[0])))
        assert res_columns == excepted_columns_contraction

    def test_merge_overlapping_columns(
        self,
        columns_for_merge_overlapping_columns,
        expected_result_for_merge_overlapping_columns,
    ):
        for columns, expected_res in zip(
            columns_for_merge_overlapping_columns,
            expected_result_for_merge_overlapping_columns,
        ):
            result = util.merge_overlapping_boxes(columns, MERGE_COLUMNS_THRESHOLD)
            assert result == expected_res

    def test_form_lines_from_columns(self):
        result = ColumnsCorrection().form_lines_from_columns(lines_from_columns)
        assert result == res_for_lines_from_columns
