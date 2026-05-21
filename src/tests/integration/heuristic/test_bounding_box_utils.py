from itertools import combinations

from deps_tables.infrastructure.heuristic.utils import (
    bounding_box_to_tuple,
    calculate_bbox_area,
    check_any_intersection,
    check_intersection_small_box_big_box,
    column_neighbor,
    cut_intersection_by_x,
    cut_intersection_by_y,
    get_intersection_area,
    get_intersection_area_coord,
    is_box_valid,
    is_intersected_by_box,
    merge_bboxes,
    row_neighbor,
)

fat_cells = [
    [300, 1600, 900, 2050],
    [600, 1700, 1200, 2000],
    [1300, 1660, 1800, 2000],
    [300, 860, 700, 1400],
    [900, 1000, 1500, 1450],
    [1200, 950, 1800, 1600],
    [1700, 1000, 2000, 1600],
]
expected_fixed_cells = [
    [300, 860, 700, 1400],
    [900, 950, 1800, 1600],
    [300, 1600, 1200, 2050],
    [1300, 1660, 1800, 2000],
    [1700, 1000, 2000, 1600],
]
reformatted_cells = [
    (39, 2829, 863, 2899),
    (0, 88, 300, 156),
    (15, 1257, 872, 1324),
    (6, 1995, 799, 2059),
    (1609, 87, 1919, 156),
    (1610, 1185, 1677, 1249),
    (1, 1109, 462, 1174),
    (958, 587, 1158, 646),
    (0, 2349, 900, 2409),
    (963, 89, 1217, 154),
    (1607, 731, 1679, 796),
    (13, 2583, 896, 2657),
    (1609, 655, 1678, 720),
    (1610, 1427, 1679, 1490),
    (5, 2424, 338, 2492),
    (0, 818, 1528, 884),
    (5, 226, 862, 293),
    (960, 660, 1161, 718),
    (1610, 1756, 1681, 1816),
    (9, 503, 641, 567),
    (10, 165, 808, 232),
    (1602, 2506, 1682, 2572),
    (1610, 197, 1678, 259),
    (1614, 2108, 1800, 2168),
    (47, 1189, 843, 1250),
    (20, 2511, 540, 2571),
    (1610, 973, 1681, 1030),
    (6, 1597, 921, 1667),
    (1610, 583, 1682, 646),
    (1611, 1297, 1682, 1357),
    (1608, 2668, 1681, 2727),
    (1, 1028, 160, 1088),
    (966, 2242, 1218, 2299),
    (1611, 1593, 1683, 1652),
    (1612, 361, 1678, 421),
    (12, 1459, 977, 1518),
    (2, 733, 554, 794),
    (2, 1646, 96, 1705),
    (1611, 1890, 1683, 1950),
    (959, 741, 1117, 795),
    (0, 1853, 717, 1917),
    (1, 663, 587, 724),
    (1, 585, 585, 645),
    (16, 2666, 773, 2736),
    (11, 318, 813, 409),
    (8, 2209, 753, 2274),
    (0, 1324, 639, 1383),
    (0, 2270, 446, 2329),
    (3, 908, 730, 970),
    (21, 2748, 798, 2816),
    (6, 425, 770, 487),
    (0, 1781, 712, 1842),
    (4, 2917, 751, 2984),
    (0, 1720, 727, 1786),
    (9, 1915, 720, 1975),
    (0, 2084, 444, 2137),
    (0, 2141, 771, 2196),
    (5, 1529, 637, 1588),
    (14, 979, 970, 1036),
]

boxes = [
    [20, 200, 200, 240],
    [35, 180, 125, 220],
    [150, 230, 160, 245],
    [190, 180, 210, 210],
    [160, 155, 180, 185],
    [40, 70, 90, 125],
    [60, 100, 110, 142],
    [130, 110, 170, 140],
]
boxes_area = [1, 1, 1, 1, 1, 1, 1, 1]
expected_res_for_check_any_intersection = [
    True,
    True,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    True,
    False,
    False,
]
expected_res_for_is_intersected_by_box = [
    True,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]
expected_res_for_get_intersection_area = [
    1800,
    100,
    100,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    750,
    0,
    0,
]
expected_res_for_calculate_bbox_area = [7200, 3600, 150, 600, 600, 2750, 2100, 1200]
expected_res_for_check_intersection_small_box_big_box = [
    1,
    1,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    0,
]
expected_res_for_get_intersection_area_coord = [
    [35, 200, 125, 220],
    [40, 200, 90, 125],
    [40, 180, 90, 125],
    [60, 200, 110, 142],
    [60, 180, 110, 142],
    [60, 100, 90, 125],
    [130, 200, 170, 140],
    [130, 180, 125, 140],
    [130, 110, 90, 125],
    [130, 110, 110, 140],
    [150, 230, 160, 240],
    [150, 230, 125, 220],
    [150, 230, 90, 125],
    [150, 230, 110, 142],
    [150, 230, 160, 140],
    [160, 200, 180, 185],
    [160, 180, 125, 185],
    [160, 230, 160, 185],
    [160, 155, 90, 125],
    [160, 155, 110, 142],
    [160, 155, 170, 140],
    [190, 200, 200, 210],
    [190, 180, 125, 210],
    [190, 230, 160, 210],
    [190, 180, 180, 185],
    [190, 180, 90, 125],
    [190, 180, 110, 142],
    [190, 180, 170, 140],
]
boxes_for_cut_intersection_by = [
    [400, 100, 900, 300],
    [300, 400, 950, 750],
    [310, 760, 1070, 850],
    [350, 1010, 950, 1340],
    [250, 1300, 840, 1600],
    [315, 1750, 890, 1980],
    [300, 1900, 900, 2200],
    [880, 990, 1400, 1410],
    [1010, 700, 1500, 1050],
    [900, 400, 1400, 1410],
    [870, 100, 1400, 370],
]
expected_column_neighbors = [
    False,
    False,
    False,
    False,
    True,
    False,
    False,
    True,
    True,
    True,
    True,
]
expected_row_neighbors = [
    True,
    True,
    True,
    True,
    False,
    True,
    True,
    False,
    False,
    True,
    True,
]
expected_rez_for_good_box = [
    False,
    False,
    True,
    False,
    False,
    True,
    False,
    False,
    False,
    False,
]
bad_boxes = [
    [-1, -3, 5, 7],
    [0, 7, 0, 7],
    [2, 10, 13, 20],
    [20, 30, 15, 40],
    [20, 30, 35, 25],
    [10, 13, 27, 23],
    [-1, 8, 3, 20],
    [23, 33, 20, 30],
    [3, -3, 8, 10],
    [-1, 5, -3, 9],
]
MERGE_CELLS_THRESHOLD = 0.4


class TestBoudingBoxUtils:
    def test_bounding_box_to_tuple(self, orig_cells):
        result_cells = bounding_box_to_tuple(orig_cells)
        assert result_cells == reformatted_cells

    def test_check_any_intersection(self):
        res = []
        for bbox1, bbox2 in combinations(boxes, 2):
            res.append(check_any_intersection(bbox1, bbox2))
        assert res == expected_res_for_check_any_intersection

    def test_is_intersected_by_box(self):
        res = []
        for bbox1, bbox2 in combinations(boxes, 2):
            res.append(is_intersected_by_box(bbox1, bbox2, 0.5))
        assert res == expected_res_for_is_intersected_by_box

    def test_merge_bboxes__simple_bboxes(self):
        bboxes = [
            [0, 0, 10, 10],
            [10, 10, 20, 20],
            [5, 0, 20, 11],
        ]
        expected_bboxes = [
            [0, 0, 20, 11],
            [10, 10, 20, 20],
        ]

        actual_bboxes = merge_bboxes(
            bboxes=bboxes,
            merge_threshold=0.4,
        )

        assert sorted(actual_bboxes) == sorted(expected_bboxes)

    def test_merge_bboxes_cells(self):
        fixed_bboxes = merge_bboxes(fat_cells, MERGE_CELLS_THRESHOLD)
        assert sorted(fixed_bboxes, key=lambda x: x[0]) == sorted(expected_fixed_cells, key=lambda x: x[0])

    def test_get_intersection_area(self):
        res = []
        for bbox1, bbox2 in combinations(boxes, 2):
            res.append(get_intersection_area(bbox1, bbox2))
        assert res == expected_res_for_get_intersection_area

    def test_calculate_bbox_area(self):
        res = []
        for bbox in boxes:
            res.append(calculate_bbox_area(bbox))
        assert res == expected_res_for_calculate_bbox_area

    def test_check_intersection_small_box_big_box(self):
        res = []
        for bbox1, bbox2 in combinations(boxes, 2):
            res.append(check_intersection_small_box_big_box(bbox1, bbox2))
        assert res == expected_res_for_check_intersection_small_box_big_box

    def test_get_intersection_area_coord(self):
        res = []
        for bbox1, bbox2 in combinations(boxes, 2):
            res.append(get_intersection_area_coord(bbox1, bbox2))
        assert sorted(res, key=lambda x: x[0]) == sorted(expected_res_for_get_intersection_area_coord, key=lambda x: x[0])

    def test_cut_intersection_by_y(self, expected_for_intersection_by_y):
        res = []
        for bbox1, bbox2 in combinations(boxes_for_cut_intersection_by, 2):
            if check_any_intersection(bbox1, bbox2) and bbox1 != bbox2:
                intersec_area = get_intersection_area_coord(bbox1, bbox2)
                right, left, new_right, new_left = cut_intersection_by_y(bbox1, bbox2, intersec_area)
                res.append([right, left, new_right, new_left])
        assert res == expected_for_intersection_by_y

    def test_cut_intersection_by_x(self, expected_for_intersection_by_x):
        res = []
        for bbox1, bbox2 in combinations(boxes_for_cut_intersection_by, 2):
            if check_any_intersection(bbox1, bbox2) and bbox1 != bbox2:
                intersec_area = get_intersection_area_coord(bbox1, bbox2)
                right, left, new_right, new_left = cut_intersection_by_x(bbox1, bbox2, intersec_area)
                res.append([right, left, new_right, new_left])
        assert res == expected_for_intersection_by_x

    def test_column_neighbor_detection(self):
        res = []
        for bbox1, bbox2 in combinations(boxes_for_cut_intersection_by, 2):
            if check_any_intersection(bbox1, bbox2) and bbox1 != bbox2:
                intersec_area = get_intersection_area_coord(bbox1, bbox2)
                res.append(column_neighbor(bbox1, bbox2))
        assert res == expected_column_neighbors

    def test_row_neighbor_detection(self):
        res = []
        for bbox1, bbox2 in combinations(boxes_for_cut_intersection_by, 2):
            if check_any_intersection(bbox1, bbox2) and bbox1 != bbox2:
                intersec_area = get_intersection_area_coord(bbox1, bbox2)
                res.append(row_neighbor(bbox1, bbox2))
        assert res == expected_row_neighbors

    def test_is_box_valid(self):
        res = []
        for box in bad_boxes:
            res.append(is_box_valid(box))
        assert res == expected_rez_for_good_box
