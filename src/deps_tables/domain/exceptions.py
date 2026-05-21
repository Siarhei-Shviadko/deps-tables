class TablesException(Exception):  # noqa: N818
    code = "tables_exception"


class TableDetectorNotFoundError(TablesException):
    code = "table_detector_not_found_error"


class ImageLoadError(TablesException):
    code = "image_load_error"


class AuthError(TablesException):
    code = "authentication_error"


class ForbiddenError(TablesException):
    code = "forbidden_error"


class ServiceProxyError(TablesException):
    code = "service_proxy_error"

    def __init__(self, status_code: int, message: str, service_name: str = None):
        if service_name is not None:
            message = f"{service_name} service says with code {status_code}: {message}"

        super().__init__(message)
