from typing import Dict, List, Optional

from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.domain.entities import ImageEntity, TableEntity
from deps_tables.domain.entities.table_detector import TableDetectorInitSettings
from deps_tables.domain.exceptions import TableDetectorNotFoundError
from deps_tables.domain.interfaces import ITableExtractor
from deps_tables.domain.services.table_identifier_service import TableIdentifierService


class TableExtractionService:
    def __init__(
        self,
        preinit_detectors: bool,
        registered_detectors: Dict[TableDetectionEngineEnum, TableDetectorInitSettings],
        enabled_detectors: List[TableDetectionEngineEnum],
        table_identifier: TableIdentifierService,
    ):
        self._enabled_detectors = set(enabled_detectors)
        self._registered_detectors = registered_detectors
        self._available_detectors: Dict[TableDetectionEngineEnum, ITableExtractor] = {}
        self._table_identifier_service = table_identifier

        if preinit_detectors:
            for detector_name, detector_settings in self._registered_detectors.items():
                self._initialize_detector(detector_name, detector_settings)

    def execute(
        self,
        *,
        image: ImageEntity,
        detector: TableDetectionEngineEnum,
        ocr_engine: str,
        language: str,
    ) -> List[TableEntity]:
        table_detector_impl = self._get_detector(detector)
        if table_detector_impl is None:
            raise TableDetectorNotFoundError(f"Table detection engine {detector} is not available")
        if not self._table_identifier_service.is_table_on_page(image.image):
            return []
        return table_detector_impl.extract_tables(image_obj=image, ocr_engine=ocr_engine, language=language)

    def _get_detector(self, detector: TableDetectionEngineEnum) -> Optional[ITableExtractor]:
        if detector not in self._available_detectors:
            registered_detector = self._registered_detectors.get(detector)
            if registered_detector:
                self._initialize_detector(detector, registered_detector)
        return self._available_detectors.get(detector, None)

    def _initialize_detector(
        self,
        detector_name: TableDetectionEngineEnum,
        detector_settings: TableDetectorInitSettings,
    ) -> None:
        if (detector_name not in self._available_detectors) and (detector_name in self._enabled_detectors):
            self._available_detectors[detector_name] = detector_settings.detector_cls(*detector_settings.detector_args)
