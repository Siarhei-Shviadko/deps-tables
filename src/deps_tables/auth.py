from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi.requests import Request

from deps_tables.containers import Application
from deps_tables.domain.exceptions import AuthError
from deps_tables.extras.auth import DepsAuthService
from deps_tables.extras.auth.exceptions import (
    EmptyAuthorizationHeader,
    InvalidAuthorizationHeaderFormat,
    InvalidJWTError,
)
from deps_tables.infrastructure.access_management.context_vars import user

PUBLIC_ENDPOINTS = (
    "/api/tables/docs",
    "/api/tables/docs/swagger-ui.css",
    "/api/tables/openapi.json",
    "/api/tables/debug/500",
    "/api/tables/healthcheck",
    "/api/tables/service-info/version",
    "/favicon.ico",
)


@inject
def set_user_from_jwt(
    request: Request,
    auth_service: DepsAuthService = Provide[Application.deps_auth_service],
) -> None:
    if request.url.path not in PUBLIC_ENDPOINTS:
        try:
            user_credentials = auth_service.authorize(request.headers)
            user.set(user_credentials)
        except (EmptyAuthorizationHeader, InvalidAuthorizationHeaderFormat) as e:
            raise AuthError(str(e))
        except InvalidJWTError:
            raise AuthError("Invalid JWT")


def get_current_user_organisation() -> Optional[str]:
    current_user = user.get(None)

    return current_user.get("organisation") if current_user is not None else None
