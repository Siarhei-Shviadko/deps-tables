from typing import Any, Dict, Optional, Type, Union

from dependency_injector import containers, providers, resources
from deps_asb import ASBClient, ASBConsumer, ASBProducer
from deps_kafka import KafkaClient, KafkaConsumer, KafkaProducer
from deps_message_flow import MessagingDriverEnum
from deps_message_flow.events.publisher import DomainEventPublisher
from deps_rabbitmq import RabbitMQClient, RabbitMQConsumer, RabbitMQProducer

from deps_tables.application import ApplicationService
from deps_tables.constants import ASB_SUBSCRIPTION_NAME
from deps_tables.domain.constants import TableDetectionEngineEnum
from deps_tables.domain.entities.table_detector import TableDetectorInitSettings
from deps_tables.domain.services.ocr_table_service import OCRTableService
from deps_tables.domain.services.table_extraction_service import TableExtractionService
from deps_tables.domain.services.table_identifier_service import TableIdentifierService
from deps_tables.events_handler.consumer import make_consumer
from deps_tables.extras.auth import DepsAuthService, JWTAuthService
from deps_tables.extras.services import OCRControllerService, StorageControllerService
from deps_tables.infrastructure.bbox_identifiers import (
    CellBorderIdentifier,
    ColumnBorderIdentifier,
    TableBorderIdentifier,
)
from deps_tables.infrastructure.services import OCRService
from deps_tables.infrastructure.services.ocr_data_converter import OCRDataConverter
from deps_tables.infrastructure.table_extractors import (
    AWSTableExtractor,
    AzureTableExtractor,
    DepsTablesExtractor,
    GCPTableExtractor,
)

MessagingClient = Union[ASBClient, KafkaClient, RabbitMQClient]


class MessageBrokerResource(resources.Resource):
    def init(
        self,
        driver_type: str,
        expected_driver: str,
        client: Type[MessagingClient],
        message_connection_string: str,
        **kwargs: Dict[str, Any],
    ) -> Optional[MessagingClient]:
        return client(message_connection_string, **kwargs) if driver_type == expected_driver else None

    def shutdown(self, resource: Optional[MessagingClient]) -> None:
        if resource:
            resource.close()


class MessageBrokers(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging_driver_settings = providers.Dependency(instance_of=object)

    broker_client: providers.Provider = providers.Selector(
        config.messaging_driver,
        asb=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.ASB.value,
            expected_driver=config.messaging_driver,
            client=ASBClient,
            message_connection_string=config.message_broker_connection_string,
            asb_settings=messaging_driver_settings,
        ),
        kafka=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.KAFKA.value,
            expected_driver=config.messaging_driver,
            client=KafkaClient,
            message_connection_string=config.message_broker_connection_string,
            settings=messaging_driver_settings,
        ),
        rabbitmq=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.RABBITMQ.value,
            expected_driver=config.messaging_driver,
            client=RabbitMQClient,
            message_connection_string=config.message_broker_connection_string,
            settings=messaging_driver_settings,
        ),
    )


class Messaging(containers.DeclarativeContainer):
    config = providers.Configuration()
    message_brokers = providers.DependenciesContainer()

    producer: providers.Provider = providers.Selector(
        config.messaging_driver,
        asb=providers.Singleton(
            ASBProducer,
            client=message_brokers.broker_client,
            topic_name=config.messaging_driver_settings.topic_name,
        ),
        kafka=providers.Singleton(
            KafkaProducer,
            client=message_brokers.broker_client,
        ),
        rabbitmq=providers.Singleton(
            RabbitMQProducer,
            client=message_brokers.broker_client,
        ),
    )
    consumer: providers.Provider = providers.Selector(
        config.messaging_driver,
        asb=providers.Singleton(
            ASBConsumer,
            client=message_brokers.broker_client,
            topic_name=config.messaging_driver_settings.topic_name,
            custom_subscription_name=ASB_SUBSCRIPTION_NAME,
        ),
        kafka=providers.Singleton(
            KafkaConsumer,
            client=message_brokers.broker_client,
        ),
        rabbitmq=providers.Singleton(
            RabbitMQConsumer,
            client=message_brokers.broker_client,
        ),
    )


class DomainEventPublishers(containers.DeclarativeContainer):
    messaging = providers.DependenciesContainer()

    publisher: providers.Singleton = providers.Singleton(
        DomainEventPublisher,
        messaging.producer,
    )


class ExternalServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    ocr_controller_service: providers.Provider = providers.Singleton(
        OCRControllerService,
        config.ocr_api_url,
    )
    storage_controller_service: providers.Provider = providers.Singleton(
        StorageControllerService,
        file_storage_url=config.file_storage_url,
        verify_ssl=config.verify_ssl,
    )


class OCRServices(containers.DeclarativeContainer):
    config = providers.Configuration()
    external_services = providers.DependenciesContainer()

    ocr: providers.Provider = providers.Singleton(
        OCRService,
        config,
        external_services.ocr_controller_service,
    )

    converter: providers.Provider = providers.Singleton(OCRDataConverter)


class CoreServices(containers.DeclarativeContainer):
    config = providers.Configuration()
    ocr_services = providers.DependenciesContainer()

    ocr_service: providers.Selector = providers.Selector(
        config.ocr_version,
        main=ocr_services.ocr,
        converter=ocr_services.converter,
    )
    table_identifier_service: providers.Provider = providers.Singleton(
        TableIdentifierService,
        table_identifier_cls=providers.Singleton(
            TableDetectorInitSettings,
            detector_cls=TableBorderIdentifier,
            detector_args=providers.List(config.table_identifier_model_weights_path, config.enable_gpu),
        ),
        enable_table_identifier=config.enable_table_border_identifier,
    )

    ocr_table: providers.Provider = providers.Singleton(OCRTableService, ocr_service)

    build_info: providers.Provider = providers.Dict(
        {
            "build_tag": config.info.tag,
            "build_date": config.info.date,
            "commit_hash": config.info.hash,
        },
    )


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()
    core = providers.DependenciesContainer()
    external_services = providers.DependenciesContainer()
    messaging = providers.DependenciesContainer()
    ocr_services = providers.DependenciesContainer()

    table_border_identifier: providers.Provider = providers.Singleton(
        TableBorderIdentifier,
        config.table_identifier_model_weights_path,
        config.enable_gpu,
    )
    column_border_identifier: providers.Provider = providers.Singleton(
        ColumnBorderIdentifier,
        config.column_identifier_model_weights_path,
        config.enable_gpu,
    )
    cell_border_identifier: providers.Provider = providers.Singleton(
        CellBorderIdentifier,
        config.cell_identifier_cfg_path,
        config.cell_identifier_weights_path,
        config.enable_gpu,
    )

    table_detection: providers.Provider = providers.Singleton(
        TableExtractionService,
        config.preinit_detectors,
        registered_detectors=providers.Dict(
            {
                TableDetectionEngineEnum.AWS_TEXTRACT: providers.Singleton(
                    TableDetectorInitSettings,
                    detector_cls=AWSTableExtractor,
                    detector_args=providers.List(
                        config.aws_region_name,
                        config.aws_access_key_id,
                        config.aws_secret_access_key,
                        core.ocr_table,
                    ),
                ),
                TableDetectionEngineEnum.AZURE_FORM_RECOGNIZER: providers.Singleton(
                    TableDetectorInitSettings,
                    detector_cls=AzureTableExtractor,
                    detector_args=providers.List(
                        config.azure_form_recognizer_api_url,
                        config.azure_form_recognizer_api_key,
                        core.ocr_table,
                    ),
                ),
                TableDetectionEngineEnum.DEPS_DETECTOR: providers.Singleton(
                    TableDetectorInitSettings,
                    detector_cls=DepsTablesExtractor,
                    detector_args=providers.List(
                        table_border_identifier,
                        column_border_identifier,
                        cell_border_identifier,
                        core.ocr_service,
                    ),
                ),
                TableDetectionEngineEnum.DEPS_CONVERTER: providers.Singleton(
                    TableDetectorInitSettings,
                    detector_cls=DepsTablesExtractor,
                    detector_args=providers.List(
                        table_border_identifier,
                        column_border_identifier,
                        cell_border_identifier,
                        ocr_services.converter,
                    ),
                ),
                TableDetectionEngineEnum.GCP_FORM_PARSER: providers.Singleton(
                    TableDetectorInitSettings,
                    detector_cls=GCPTableExtractor,
                    detector_args=providers.List(
                        config.gcp_project_id,
                        config.gcp_location,
                        config.gcp_processor_id,
                        config.gcp_api_key,
                        core.ocr_table,
                    ),
                ),
            },
        ),
        enabled_detectors=config.enabled_detectors,
        table_identifier=core.table_identifier_service,
    )

    consumer: providers.Singleton = providers.Singleton(make_consumer, messaging.consumer)


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging_driver_settings = providers.Dependency(instance_of=object)
    external_services = providers.Container(ExternalServices, config=config)
    ocr_services = providers.Container(OCRServices, config=config, external_services=external_services)
    core = providers.Container(CoreServices, config=config, ocr_services=ocr_services)
    message_brokers: providers.Container = providers.Container(
        MessageBrokers,
        config=config,
        messaging_driver_settings=messaging_driver_settings,
    )
    messaging: providers.Container = providers.Container(
        Messaging,
        config=config,
        message_brokers=message_brokers,
    )
    event_publisher: providers.Container = providers.Container(
        DomainEventPublishers,
        messaging=messaging,
    )
    services = providers.Container(
        Services,
        config=config,
        core=core,
        external_services=external_services,
        messaging=messaging,
        ocr_services=ocr_services,
    )

    application: providers.Provider = providers.Singleton(
        ApplicationService,
        table_extraction_service=services.table_detection,
        ocr_table_service=core.ocr_table,
    )

    jwt_auth_service: providers.Provider = providers.Singleton(
        JWTAuthService,
        config.authentication.certs_endpoint,
        config.authentication.encryption_algorithm,
        config.authentication.verify_ssl,
    )

    deps_auth_service: providers.Provider = providers.Singleton(
        DepsAuthService,
        jwt_auth_service,
    )
