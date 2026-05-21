import cv2
import numpy as np
import pytest

from deps_tables.infrastructure.heuristic.image_processing import (
    adaptive_threshold,
    detect_lines_with_cv2,
    find_lines,
    image_processing,
)
from deps_tables.infrastructure.heuristic.utils import create_table_from_lines

rows = [
    [0, 49],
    [49, 124],
    [124, 199],
    [199, 274],
    [274, 349],
    [349, 424],
    [424, 499],
    [499, 574],
    [574, 649],
    [649, 724],
    [724, 799],
    [799, 873],
    [873, 948],
    [948, 1023],
    [1023, 1098],
    [1098, 1173],
    [1173, 1248],
    [1248, 1323],
    [1323, 1454],
    [1454, 1586],
    [1586, 1661],
    [1661, 1735],
    [1735, 1810],
    [1810, 1885],
    [1885, 1960],
    [1960, 2035],
    [2035, 2110],
    [2110, 2185],
    [2185, 2260],
    [2260, 2335],
    [2335, 2410],
    [2410, 2485],
    [2485, 2560],
    [2560, 2635],
    [2635, 2710],
    [2710, 2785],
    [2785, 2860],
    [2860, 3300],
]
columns = [[3, 0, 993, 2917], [1478, 0, 2210, 2922], [986, 5, 1482, 2922]]
expected_intervals = [
    [0, 58],
    [61, 114],
    [126, 188],
    [193, 257],
    [257, 321],
    [325, 386],
    [386, 452],
    [452, 514],
    [518, 582],
    [582, 646],
    [650, 712],
    [712, 777],
    [777, 839],
    [843, 907],
    [907, 1080],
]


class TestLinesDetection:
    def test_adaptive_threshold__with_lines(self):
        image_path = "tests/data/image_with_lines.jpg"
        img_vector = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img, threshold = adaptive_threshold(img_vector, process_background=False, blocksize=15, c=-2)
        assert img.shape == (2200, 1700)
        assert threshold.shape == (2200, 1700)  # (1418, 1961)

    def test_line_detection__with_lines(self):
        with open("tests/data/threshold.npy", "rb") as f:
            threshold = np.load(f)
        dmask1, lines_h = find_lines(threshold, regions=None, direction="horizontal", line_scale=15, iterations=0)
        assert len(lines_h) > 3

    def test_image_processing__without_lines(self):
        image_path = "tests/data/image_without_lines.jpg"
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        lines_h = image_processing(img)
        assert len(lines_h) < 3

    def test_create_table_from_lines(self, exp_cv2_cells):
        new_cells = create_table_from_lines(columns, rows)
        for key in exp_cv2_cells.keys():
            assert new_cells[key] == exp_cv2_cells[key]

    @pytest.mark.skip
    def test_detect_lines_with_cv2(self, lines_h, cells_for_lines_detection_with_cv2, ocr):
        image_path = "tests/data/10_25_2021 - image001.png"
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        crop_img = img[18:1111, 48:1927]
        y_coords = []
        y_coords.extend([line[1] for line in lines_h])
        filtered_y_coords = list(set(y_coords))
        rows_intervals = detect_lines_with_cv2(filtered_y_coords, crop_img, cells_for_lines_detection_with_cv2, ocr)
        assert rows_intervals == expected_intervals
