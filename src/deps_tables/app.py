from typing import Optional

from deps_tables import api, auth
from deps_tables.containers import Application
from deps_tables.events_handler import handlers
from deps_tables.infrastructure import services as infrastructure_services
from deps_tables.infrastructure.access_management import table_detection_engine_accessor
from deps_tables.infrastructure.access_management.context_vars import user
from deps_tables.settings import Settings


def init_application(settings: Optional[Settings] = None) -> Application:
    if not settings:
        settings = Settings()
    app = Application(messaging_driver_settings=settings.messaging_driver_settings)
    app.config.from_pydantic(settings)
    app.init_resources()
    if app.config.authentication.enabled():
        app.external_services.ocr_controller_service().set_user_context(user)
        app.external_services.storage_controller_service().set_user_context(user)
        app.message_brokers.broker_client().user_context = user
    app.wire(
        packages=[api, infrastructure_services],
        modules=[auth, handlers, table_detection_engine_accessor],
    )
    app.services.wire(packages=[api], modules=[handlers])
    app.event_publisher.wire(modules=[handlers])

    return app
