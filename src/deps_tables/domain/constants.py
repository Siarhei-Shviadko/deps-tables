from enum import Enum


class TableDetectionEngineEnum(str, Enum):
    AWS_TEXTRACT = "AWS_TEXTRACT"
    AZURE_FORM_RECOGNIZER = "AZURE_FORM_RECOGNIZER"
    GCP_FORM_PARSER = "GCP_FORM_PARSER"
    DEPS_DETECTOR = "DEPS_DETECTOR"
    DEPS_CONVERTER = "DEPS_CONVERTER"


BIND = "0.0.0.0:8000"
WORKER_CLASS = "uvicorn.workers.UvicornWorker"
PROJECT_NAME = "DEPS Table Service"
PROJECT_DESCRIPTION = "Table service for extracting tables from image using different OCR and table detection engines."
API_PREFIX = "/api/tables"
SWAGGER_DOC_URL = "/docs"

DEFAULT_TABLE_DETECTOR = TableDetectionEngineEnum.DEPS_DETECTOR
DEFAULT_OCR_ENGINE = "TESSERACT"
AWS_OCR_ENGINE = "AWS_TEXTRACT"
GCP_OCR_ENGINE = "GCP_VISION"
AZURE_OCR_ENGINE = "AZURE_FORM_RECOGNIZER"
DEFAULT_LANGUAGE = "eng"

TABLE_IDENTIFIER_MODEL_WEIGHTS_PATH = "/models/detectron_tables_model.pth"
COLUMN_IDENTIFIER_MODEL_WEIGHTS_PATH = "/models/detectron_columns_model.pth"
CELL_IDENTIFIER_CFG_PATH = "/models/yolo/yolo-obj.cfg"
CELL_IDENTIFIER_WEIGHTS_PATH = "/models/yolo/yolo-obj_6000.weights"
