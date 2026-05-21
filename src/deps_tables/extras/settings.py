from typing import Optional

from pydantic import BaseSettings, Field, root_validator


class SentrySettings(BaseSettings):
    enabled: bool = False
    trace_enabled: bool = False
    dsn: Optional[str] = None
    traces_sample_rate: Optional[float] = 0

    class Config:
        env_prefix = "SENTRY_"
        allow_mutation = False


class AuthenticationSettings(BaseSettings):
    enabled: bool = Field(False, env="AUTH_ENABLED")
    verify_ssl: bool = Field(True, env="AUTH_VERIFY_SSL")
    certs_endpoint: str = Field(None, env="AUTH_CERTS_ENDPOINT")
    encryption_algorithm: str = Field("RS256", env="AUTH_ENCRYPTION_ALGORITHM")
    api_key: str = Field(None, env="API_KEY")

    @root_validator
    def validate_certs_endpoint_and_key(cls, values):  # noqa: N805, WPS110
        if values["enabled"] and (values["certs_endpoint"] is None and values["api_key"] is None):
            raise ValueError(
                "Please provide OAUTH certificates endpoint via `AUTH_CERTS_ENDPOINT` or provide auth key via `API_KEY`",
            )
        return values


class ServiceInfoSettings(BaseSettings):
    tag: str = ""
    date: str = ""
    hash: str = ""

    class Config:
        env_prefix = "SERVICE_INFO_"
