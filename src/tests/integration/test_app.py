import numpy as np

from deps_tables.domain.entities import (
    AbsoluteAreaEntity,
    ImageEntity,
    ImageMetadataEntity,
)
from deps_tables.extras.ocr import Point, Rectangle, TextLine, WordBox


class TestApplicationService:
    def test_get_detected_tables__without_selected_area__image_and_meta_not_changed(self, application_service, tds_mock):
        meta = ImageMetadataEntity(
            textlines=[
                TextLine(
                    id=1,
                    word_boxes=[
                        self._build_wordbox(
                            content="a",
                            area=AbsoluteAreaEntity(left=10, top=20, width=10, height=10),
                        ),
                        self._build_wordbox(
                            content="b",
                            area=AbsoluteAreaEntity(left=20, top=10, width=10, height=10),
                        ),
                    ],
                ),
                TextLine(
                    id=2,
                    word_boxes=[
                        self._build_wordbox(
                            content="b",
                            area=AbsoluteAreaEntity(left=50, top=60, width=10, height=10),
                        ),
                    ],
                ),
            ]
        )
        image = ImageEntity(
            image=np.zeros((100, 200)),
            blob_path=None,
            meta=meta,
        )

        tds_mock.execute.return_value = []

        expected_surface = np.zeros((100, 200))
        expected_meta = ImageMetadataEntity(
            textlines=[
                TextLine(
                    id=1,
                    word_boxes=[
                        self._build_wordbox(
                            content="a",
                            area=AbsoluteAreaEntity(left=10, top=20, width=10, height=10),
                        ),
                        self._build_wordbox(
                            content="b",
                            area=AbsoluteAreaEntity(left=20, top=10, width=10, height=10),
                        ),
                    ],
                ),
                TextLine(
                    id=2,
                    word_boxes=[
                        self._build_wordbox(
                            content="b",
                            area=AbsoluteAreaEntity(left=50, top=60, width=10, height=10),
                        ),
                    ],
                ),
            ]
        )
        expected_image = ImageEntity(
            image=expected_surface,
            blob_path=None,
            meta=expected_meta,
        )

        application_service().detect_tables(
            image=image,
            table_detection_engine=None,
            ocr_engine=None,
            language=None,
            selected_area=None,
        )

        called_image = tds_mock.execute.call_args_list[0][1]["image"]

        assert np.all(called_image.image == expected_image.image)
        assert called_image.meta == expected_meta

    def test_get_detected_tables__with_selected_area__image_subbed_and_meta_shifted(self, application_service, tds_mock):
        meta = ImageMetadataEntity(
            textlines=[
                TextLine(
                    id=1,
                    word_boxes=[
                        self._build_wordbox(
                            content="a",
                            area=AbsoluteAreaEntity(left=10, top=20, width=10, height=10),
                        ),
                        self._build_wordbox(
                            content="b",
                            area=AbsoluteAreaEntity(left=20, top=10, width=10, height=10),
                        ),
                    ],
                ),
                TextLine(
                    id=2,
                    word_boxes=[
                        self._build_wordbox(
                            content="b",
                            area=AbsoluteAreaEntity(left=50, top=60, width=10, height=10),
                        ),
                    ],
                ),
            ]
        )
        image = ImageEntity(
            image=np.zeros((100, 200)),
            blob_path=None,
            meta=meta,
        )

        selected_area = AbsoluteAreaEntity(left=30, top=40, width=50, height=60)

        tds_mock.execute.return_value = []

        expected_surface = np.zeros((60, 50))
        expected_meta = ImageMetadataEntity(
            textlines=[
                TextLine(
                    id=1,
                    word_boxes=[
                        self._build_wordbox(
                            content="a",
                            area=AbsoluteAreaEntity(left=-20, top=-20, width=10, height=10),
                        ),
                        self._build_wordbox(
                            content="b",
                            area=AbsoluteAreaEntity(left=-10, top=-30, width=10, height=10),
                        ),
                    ],
                ),
                TextLine(
                    id=2,
                    word_boxes=[
                        self._build_wordbox(
                            content="b",
                            area=AbsoluteAreaEntity(left=20, top=20, width=10, height=10),
                        ),
                    ],
                ),
            ]
        )
        expected_image = ImageEntity(
            image=expected_surface,
            blob_path=None,
            meta=expected_meta,
        )

        application_service().detect_tables(
            image=image,
            table_detection_engine=None,
            ocr_engine=None,
            language=None,
            selected_area=selected_area,
        )

        called_image = tds_mock.execute.call_args_list[0][1]["image"]

        assert np.all(called_image.image == expected_image.image)
        assert called_image.meta == expected_meta

    def test_get_detected_tables__with_selected_area_and_meta_is_none__image_subbed(self, application_service, tds_mock):
        image = ImageEntity(
            image=np.zeros((100, 200)),
            blob_path=None,
            meta=None,
        )

        selected_area = AbsoluteAreaEntity(left=30, top=40, width=50, height=60)

        tds_mock.execute.return_value = []

        expected_surface = np.zeros((60, 50))
        expected_image = ImageEntity(
            image=expected_surface,
            blob_path=None,
            meta=None,
        )

        application_service().detect_tables(
            image=image,
            table_detection_engine=None,
            ocr_engine=None,
            language=None,
            selected_area=selected_area,
        )

        called_image = tds_mock.execute.call_args_list[0][1]["image"]

        assert np.all(called_image.image == expected_image.image)
        assert called_image.meta == None

    def test_get_detected_tables__with_selected_area_textlines_is_none__image_subbed(self, application_service, tds_mock):
        meta = ImageMetadataEntity(
            textlines=None,
        )
        image = ImageEntity(
            image=np.zeros((100, 200)),
            blob_path=None,
            meta=meta,
        )

        selected_area = AbsoluteAreaEntity(left=30, top=40, width=50, height=60)

        tds_mock.execute.return_value = []

        expected_surface = np.zeros((60, 50))
        expected_meta = ImageMetadataEntity(
            textlines=None,
        )
        expected_image = ImageEntity(
            image=expected_surface,
            blob_path=None,
            meta=expected_meta,
        )

        application_service().detect_tables(
            image=image,
            table_detection_engine=None,
            ocr_engine=None,
            language=None,
            selected_area=selected_area,
        )

        called_image = tds_mock.execute.call_args_list[0][1]["image"]

        assert np.all(called_image.image == expected_image.image)
        assert called_image.meta == expected_image.meta

    def _build_wordbox(self, content: str, area: AbsoluteAreaEntity) -> WordBox:
        return WordBox(
            content=content,
            bbox=self._convert_absolute_area_to_rect(area),
            confidence=1.0,
        )

    def _convert_absolute_area_to_rect(self, area: AbsoluteAreaEntity) -> Rectangle:
        return Rectangle(
            left_top_point=Point(
                x=area.left,
                y=area.top,
            ),
            right_bottom_point=Point(
                x=area.right,
                y=area.bottom,
            ),
        )
