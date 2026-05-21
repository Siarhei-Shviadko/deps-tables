import logging
from dataclasses import asdict
from typing import Any, Dict, List, Optional
from uuid import uuid4

import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from deps_message_flow.events.publisher import DomainEventPublisher
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_tables.api.models.image import ImageModel
from deps_tables.api.models.table import TableModel
from deps_tables.constants import PARSED_DATA_AGGREGATE
from deps_tables.containers import Application, DomainEventPublishers, Services
from deps_tables.domain.constants import (
    AWS_OCR_ENGINE,
    AZURE_OCR_ENGINE,
    DEFAULT_LANGUAGE,
    DEFAULT_OCR_ENGINE,
    DEFAULT_TABLE_DETECTOR,
    GCP_OCR_ENGINE,
    TableDetectionEngineEnum,
)
from deps_tables.domain.entities import ImageEntity, ImageMetadataEntity, TableEntity
from deps_tables.domain.events import OCRCompleted, TablesCompleted
from deps_tables.domain.services import TableExtractionService
from deps_tables.events_handler.models import ParsedTextLineModel
from deps_tables.extras.services import StorageControllerService
from deps_tables.infrastructure.access_management.table_detection_engine_accessor import (
    check_user_has_permission_to_engine,
)

_logger = logging.getLogger(__name__)


@inject
def ocr_completed_handler(
    dee: DomainEventEnvelope[OCRCompleted],
    publisher: DomainEventPublisher = Provide[DomainEventPublishers.publisher],
    tables: TableExtractionService = Provide[Services.table_detection],
) -> None:
    if not dee.event.extraction_params.get("tables"):
        return

    source_id = dee.event.source_id
    ocr_data = dee.event.ocr_data
    file_path = dee.event.file_path
    ocr_engine = dee.event.extraction_params.get("ocr_engine", DEFAULT_OCR_ENGINE)
    detector = _choose_table_detector(dee.event.extraction_params.get("table_detection_engine"), ocr_engine)
    language = dee.event.extraction_params.get("language", DEFAULT_LANGUAGE)

    check_user_has_permission_to_engine(detector)

    _logger.info("Starting table detection for source with id '%s'", source_id)
    tables_data = []
    if ocr_data:
        image = _get_image_from_storage(file_path)
        text_line_models = [ParsedTextLineModel(**data).to_text_line_model() for data in ocr_data]
        image.meta = ImageMetadataEntity(text_line_models=text_line_models)
        table_entities = tables.execute(image=image, detector=detector, ocr_engine=ocr_engine, language=language)
        tables_data = _get_tables_data_from_table_models(table_entities, source_id)

    publisher.publish(
        PARSED_DATA_AGGREGATE,
        source_id,
        [
            TablesCompleted(
                document_id=dee.event.document_id,
                source_id=source_id,
                file_path=file_path,
                extraction_params=dee.event.extraction_params,
                tables_data=tables_data,
                identify_document=dee.event.identify_document,
                extract_data=dee.event.extract_data,
                document_type=dee.event.document_type,
            ),
        ],
        headers={"ID": uuid4().hex},
    )
    _logger.info("Table detection has finished for source with id '%s'", source_id)


@inject
def _choose_table_detector(
    table_detection_engine: Optional[TableDetectionEngineEnum],
    ocr_engine: str,
    enabled_detectors: List[TableDetectionEngineEnum] = Provide[Services.config.enabled_detectors],
) -> TableDetectionEngineEnum:
    engine_to_detector_mapping = {
        AWS_OCR_ENGINE: TableDetectionEngineEnum.AWS_TEXTRACT,
        GCP_OCR_ENGINE: TableDetectionEngineEnum.GCP_FORM_PARSER,
        AZURE_OCR_ENGINE: TableDetectionEngineEnum.AZURE_FORM_RECOGNIZER,
    }

    if ocr_engine in engine_to_detector_mapping and engine_to_detector_mapping[ocr_engine] in enabled_detectors:
        return engine_to_detector_mapping[ocr_engine]

    return table_detection_engine or DEFAULT_TABLE_DETECTOR


@inject
def _get_image_from_storage(
    file_path: str,
    storage: StorageControllerService = Provide[Application.external_services.storage_controller_service],
) -> ImageEntity:
    file_content = storage.download_content(file_path=file_path)
    np_array = np.frombuffer(file_content, dtype=np.uint8)
    cv2_image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)

    return ImageModel(image=cv2_image, blob_path=file_path).to_domain()


def _get_tables_data_from_table_models(tables: List[TableEntity], source_id: str) -> List[Dict[str, Any]]:
    dicts = []
    for table in tables:
        table_dict = TableModel(**asdict(table)).dict(by_alias=True)
        table_dict["sourceId"] = source_id
        del table_dict["coordinates"]["page"]
        dicts.append(table_dict)

    return dicts
