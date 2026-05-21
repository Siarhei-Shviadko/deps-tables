import logging
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette import status
from starlette.requests import Request

from deps_tables.api.error import ErrorModel
from deps_tables.domain.exceptions import (
    ForbiddenError,
    ImageLoadError,
    ServiceProxyError,
    TableDetectorNotFoundError,
    TablesException,
)

logger = logging.getLogger(__name__)


def json_error_handler(error: TablesException, status_code: int):
    return JSONResponse(status_code=status_code, content=ErrorModel(code=error.code, message=str(error)).dict())  # noqa: WPS221


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(TablesException)
    def handle_tables_exception(req: Request, error: TablesException):
        mapper = [
            (TableDetectorNotFoundError, HTTPStatus.NOT_FOUND),
            (ImageLoadError, HTTPStatus.BAD_REQUEST),
            (ServiceProxyError, HTTPStatus.INTERNAL_SERVER_ERROR),
            (ForbiddenError, HTTPStatus.FORBIDDEN),
            (TablesException, HTTPStatus.BAD_REQUEST),
        ]

        for error_type, status_code in mapper:
            if issubclass(type(error), error_type):
                return json_error_handler(error, status_code)

    @app.exception_handler(Exception)
    def handle_all_errors(req: Request, error: Exception):
        logger.error(f"Unhandled error {error}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorModel(code="unhandled_error", message=str(error)).dict(),
        )
