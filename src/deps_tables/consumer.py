import logging

from deps_tables.app import init_application
from deps_tables.containers import Application
from deps_tables.settings import Settings

_logger = logging.getLogger(__name__)


def run_consumer() -> None:
    settings = Settings()
    settings.ocr_version = "converter"
    app: Application = init_application(settings)

    if app.config.sentry.enabled():
        import sentry_sdk  # noqa: WPS433

        sentry_sdk.init(
            dsn=app.config.sentry.dsn(),
            traces_sample_rate=app.config.sentry.traces_sample_rate(),
            environment=app.config.env(),
            release=app.config.service_info.hash(),
            debug=True,
        )

        _logger.info("SENTRY ENABLED!")

    consumer = app.services.consumer()
    consumer.start_consuming()
