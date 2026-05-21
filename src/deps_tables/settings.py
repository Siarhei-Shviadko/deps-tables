from typing import Any, List

from deps_asb import ASBSettings
from deps_kafka import KafkaSettings
from deps_message_flow import MessagingDriverEnum
from deps_rabbitmq import RabbitMQTLSSettings
from pydantic import BaseSettings, Field, validator

from deps_tables.domain.constants import (
    API_PREFIX,
    BIND,
    CELL_IDENTIFIER_CFG_PATH,
    CELL_IDENTIFIER_WEIGHTS_PATH,
    COLUMN_IDENTIFIER_MODEL_WEIGHTS_PATH,
    DEFAULT_TABLE_DETECTOR,
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    SWAGGER_DOC_URL,
    TABLE_IDENTIFIER_MODEL_WEIGHTS_PATH,
    WORKER_CLASS,
    TableDetectionEngineEnum,
)
from deps_tables.extras.settings import (
    AuthenticationSettings,
    SentrySettings,
    ServiceInfoSettings,
)


class GunicornSettings(BaseSettings):
    bind: str = BIND
    workers: int = Field(..., env="WORKERS")
    reload: bool = Field(False, env="RELOAD")
    log_level: str = Field("info", env="LOG_LEVEL")
    capture_output: bool = True
    worker_class: str = WORKER_CLASS
    max_requests: int = Field(..., env="MAX_REQUESTS")
    timeout: int = Field(..., env="TIMEOUT")


class Settings(BaseSettings):
    env: str = "development"
    project_name: str = PROJECT_NAME
    description: str = PROJECT_DESCRIPTION
    version: str = Field(..., env="PROJECT_VERSION")
    api_prefix: str = API_PREFIX
    swagger_doc_url: str = SWAGGER_DOC_URL

    ocr_api_url: str = Field(None, env="OCR_API_URL")

    aws_region_name: str = Field(..., env="AWS_REGION_NAME")
    aws_access_key_id: str = Field(..., env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")

    azure_form_recognizer_api_url: str = Field(..., env="AZURE_FORM_RECOGNIZER_API")
    azure_form_recognizer_api_key: str = Field(..., env="AZURE_FORM_RECOGNIZER_KEY")

    gcp_project_id: str
    gcp_location: str
    gcp_processor_id: str
    gcp_api_key: str

    file_storage: str = Field(..., env="BLOB_STORAGE")
    file_storage_url: str = Field(..., env="FILE_STORAGE_URL")
    verify_sll: bool = Field(True)
    preinit_detectors: bool = Field(False, env="PREINIT_DETECTORS")
    queue_name: str = Field("table_detection", env="QUEUE_NAME")
    default_detector: TableDetectionEngineEnum = DEFAULT_TABLE_DETECTOR
    enabled_detectors: List[TableDetectionEngineEnum] = Field(
        list(TableDetectionEngineEnum),
        env="ENABLED_DETECTION_ENGINES",
    )
    paid_engines_restriction_enabled: bool = Field(True)
    privileged_group: str = Field("deps-admins")

    enable_table_border_identifier: bool = Field(True, env="IDENTIFY_TABLE_BORDERS")
    table_identifier_model_weights_path: str = TABLE_IDENTIFIER_MODEL_WEIGHTS_PATH
    column_identifier_model_weights_path: str = COLUMN_IDENTIFIER_MODEL_WEIGHTS_PATH
    cell_identifier_cfg_path: str = CELL_IDENTIFIER_CFG_PATH
    cell_identifier_weights_path: str = CELL_IDENTIFIER_WEIGHTS_PATH

    enable_gpu: bool

    debug: bool = Field(False, env="DEBUG")
    gunicorn: GunicornSettings = GunicornSettings()
    info: ServiceInfoSettings = ServiceInfoSettings()
    authentication: AuthenticationSettings = AuthenticationSettings()
    sentry: SentrySettings = SentrySettings()

    messaging_driver: MessagingDriverEnum = Field(MessagingDriverEnum.RABBITMQ, env="MESSAGING_DRIVER")
    messaging_driver_settings: Any = Field(None, env="MESSAGING_DRIVER_SETTINGS")
    message_broker_connection_string: str

    logger_level: str = Field("INFO", env="LOG_LEVEL")
    ocr_version: str = "main"

    class Config:
        use_enum_values = True

    @validator("messaging_driver_settings")
    def validate_messaging_driver_settings(cls, v, values):  # noqa: N805, WPS110
        messaging_driver = values.get("messaging_driver")
        if not messaging_driver:
            raise ValueError("Invalid messaging driver")

        driver = MessagingDriverEnum(messaging_driver)
        if driver == MessagingDriverEnum.ASB:
            return ASBSettings()
        elif driver == MessagingDriverEnum.KAFKA:
            return KafkaSettings()
        elif driver == MessagingDriverEnum.RABBITMQ:
            return RabbitMQTLSSettings().dict()  # TODO: use BaseSettings

        raise ValueError(f"Driver {driver} is not implemented")
