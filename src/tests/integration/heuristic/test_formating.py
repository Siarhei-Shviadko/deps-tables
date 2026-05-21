import cv2

from deps_tables.infrastructure.heuristic.types import TableElements
from deps_tables.infrastructure.heuristic.utils import (
    building_output,
    cell_to_content,
    create_table_from_lines,
    reformat_ocr_output,
    resize_cells,
    resize_ocr_cells,
    sort_text_in_the_cell,
)

reformatted_ocr = [
    {"bbox": [562, 366, 720, 416], "content": "fenofibric", "line": 46},
    {"bbox": [729, 366, 800, 416], "content": "acid", "line": 46},
    {"bbox": [808, 366, 858, 416], "content": "tab", "line": 46},
    {"bbox": [866, 366, 908, 416], "content": "35", "line": 46},
    {"bbox": [916, 366, 975, 416], "content": "mg,", "line": 46},
    {"bbox": [987, 366, 1041, 416], "content": "105", "line": 46},
    {"bbox": [1054, 366, 1104, 416], "content": "mg", "line": 46},
    {"bbox": [562, 416, 745, 466], "content": "gemfibrozil", "line": 45},
    {"bbox": [1695, 416, 1800, 466], "content": "LOPID", "line": 45},
]

rows = [
    [0, 75],
    [75, 162],
    [162, 295],
    [295, 486],
    [486, 573],
    [573, 648],
    [648, 723],
    [723, 800],
    [800, 901],
    [901, 1092],
    [1092, 1179],
    [1179, 1254],
    [1254, 1388],
    [1388, 1522],
    [1522, 1713],
    [1713, 1846],
    [1846, 1980],
    [1980, 2067],
    [2067, 2200],
    [2200, 2334],
    [2334, 2410],
    [2410, 2497],
    [2497, 2572],
    [2572, 2660],
    [2660, 2801],
    [2801, 2815],
    [2815, 2908],
    [2908, 2981],
    [2981, 3300],
]
expected_sorted_text = [
    "MG, 30 MG, 45 MG, 7.5 MG",
    "ELIGARD SUBCUTANEOUS KIT 22.5",
    "10000000 UNIT/ML, 6000000 UNIT/ML",
    "INTRON A INJECTION SOLUTION",
    "MG",
    "INTRAMUSCULAR KIT 11.25 MG, 22.5",
    "80 MG",
    "SOLUTION RECONSTITUTED 120 MG,",
    "INTRAMUSCULAR KIT 45 MG",
    "LUPRON DEPOT (6-MONTH)",
    "mg/ml, 400 mg/10ml",
    "megestrol acetate oral suspension 40",
    "INTRAMUSCULAR KIT 30 MG",
    "LUPRON DEPOT (4-MONTH)",
    "*Antiparkinson Dopaminergics***",
    "Drug Name",
    "*Progestins-Antineoplastic***",
    "Restrictions",
    "PA",
    "*Lhrh Analogs***",
    "Arimidex",
    "megestrol acetate oral tablet 20 mg, 40 mg",
    "Reference",
    "PA",
    "*Urinary Tract Protective Agents***",
    "PA",
    "PA",
    "*Retinoids***",
    "*Gonadotropin Releasing Hormone (Gnrh) Antagonists***",
    "Aromasin",
    "PA",
    "*Aromatase Inhibitors***",
    "PA",
    "PA",
    "Preferred",
    "leuprolide acetate injection kit 1 mg/0.2ml",
    "tretinoin oral capsule 10 mg",
    "PA",
    "PA",
    "PA",
    "PA",
    "Megace Oral",
    "PA",
    "PA",
    "INTRAMUSCULAR KIT 3.75 MG, 7.5 MG",
    "letrozole oral tablet 2.5 mg",
    "PA",
    "Femara",
    "exemestane oral tablet 25 mg",
    "anastrozole oral tablet 1 mg",
    "MESNEX ORAL TABLET 400 MG",
    "INTRON A INJECTION SOLUTIONRECONSTITUTED 10000000 UNIT,",
    "FIRMAGON SUBCUTANEOUS",
    "*ANTIPARKINSON AGENTS*",
    "18000000 UNIT, 50000000 UNIT",
    "amantadine hcl oral capsule 100 mg",
    "hydroxyprogesterone",
    "intramuscular solution 1.25 gm/5ml",
    "LUPRON DEPOT (3-MONTH)",
]
columns = [[944, 0, 1585, 3000], [1579, 0, 2269, 2960], [7, 8, 998, 2996]]
resized_columns = [[0, 1579], [1579, 7], [7, 2418]]
table_h = 76
table_w = 138
table_box = [138, 76, 2418, 3081]
cell_threshold = 0.3


class TestFormatingMethodsFromUtils:
    def test_reformat_ocr_output(self, raw_ocr):
        new_ocr = reformat_ocr_output(raw_ocr)
        assert new_ocr == reformatted_ocr

    def test_cell_to_content(self, ocr, cell_to_content_result, resized_cells):
        cell_to_cont = cell_to_content(resized_cells, ocr, table_h, table_w, cell_threshold)
        for box in cell_to_content_result.keys():
            assert cell_to_cont[box] == cell_to_content_result[box]

    def test_resize_cells(self, bouding_to_list_cells, new_resized_cells):
        res_cells = resize_cells(bouding_to_list_cells)
        for res_cell, expected in zip(
            sorted(res_cells, key=lambda x: x[0]),
            sorted(new_resized_cells, key=lambda x: x[0]),
        ):
            assert list(res_cell) == list(expected)

    def test_resize_ocr_cells(self, ocr, resized_ocr):
        res_cells = resize_ocr_cells(ocr)
        assert sorted(res_cells, key=lambda x: x["bbox"][0]) == sorted(resized_ocr, key=lambda x: x["bbox"][0])

    def test_sort_tex_in_the_cell(self, cell_to_content_result):
        cells_text_res = []
        for cell in cell_to_content_result.keys():
            text = sort_text_in_the_cell(cell_to_content_result, cell, True)
            cells_text_res.append(text)
        assert cells_text_res == expected_sorted_text

    def test_building_output(self, resized_cells, ocr):
        image_path = "tests/data/MPC-Approved_Drug_List-1-31-1_cutted.png"
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        table_elements = TableElements(
            rows=rows,
            columns=resized_columns,
            cells=resized_cells,
            table=table_box,
            image=img,
        )
        img_shape = (table_box[3], table_box[2])
        output = building_output(table_elements, ocr, "not cv2", True, img_shape)
        row_indexes = [cell.coordinates.row for cell in output.cells]
        col_indexes = [cell.coordinates.column for cell in output.cells]
        assert all([0 <= ind for ind in row_indexes])
        assert all([0 <= ind for ind in col_indexes])

    def test_create_table_from_lines(
        self,
        columns_for_table_from_lines,
        rows_for_table_from_lines,
        expected_table_from_lines,
    ):
        for col, row, expected_res in zip(
            columns_for_table_from_lines,
            rows_for_table_from_lines,
            expected_table_from_lines,
        ):
            table = create_table_from_lines(col, row)
            assert list(table.keys()) == expected_res
