import logging
from http import HTTPStatus
from typing import Optional

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from deps_tables import Settings, api, auth
from deps_tables.app import init_application
from deps_tables.domain.exceptions import AuthError
from deps_tables.error_handlers import json_error_handler, register_error_handlers
from deps_tables.extras.fastapi_utils import add_auth_to_openapi

logger = logging.getLogger(__name__)


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    app = init_application(settings)
    fastapi_app = FastAPI(
        title=app.config.project_name(),
        version=app.config.version(),
        docs_url=f"{app.config.api_prefix()}{app.config.swagger_doc_url()}",
        description=app.config.description(),
        openapi_url=f"{app.config.api_prefix()}/openapi.json",
    )
    fastapi_app.include_router(api.router, prefix=app.config.api_prefix())
    register_error_handlers(fastapi_app)

    if app.config.sentry.enabled():
        import sentry_sdk  # noqa: WPS433
        from sentry_sdk.integrations.asgi import SentryAsgiMiddleware  # noqa: WPS433

        sentry_sdk.init(
            dsn=app.config.sentry.dsn(),
            traces_sample_rate=app.config.sentry.traces_sample_rate(),
            environment=app.config.env(),
            release=app.config.info.hash(),
            debug=True,
        )
        fastapi_app.add_middleware(SentryAsgiMiddleware)

        logger.info("SENTRY ENABLED!")

    fastapi_app.app = app  # type: ignore[attr-defined]
    register_auth(fastapi_app)

    return fastapi_app


def register_auth(app: FastAPI) -> None:
    if app.app.config.authentication.enabled():  # type: ignore
        add_auth_to_openapi(app)

        logger.info("Authentication enabled")

        @app.middleware("http")
        async def auth_middleware(request: Request, call_next) -> JSONResponse:  # noqa: WPS430
            try:
                auth.set_user_from_jwt(request)
            except AuthError as exc:
                return json_error_handler(exc, HTTPStatus.UNAUTHORIZED)
            return await call_next(request)
