def test_extraction__no_mocks__correctly_extracted(
    ocr_table_service, ocr_service, bbox_table, textlines_for_bbox_table, empty_bbox_table, image
):

    ocr_service.add_textlines(image.blob_path, textlines_for_bbox_table)
    table = ocr_table_service.extract_data_from_table(image=image, engine="TESSERACT", language="eng", table=empty_bbox_table)
    assert table == bbox_table
