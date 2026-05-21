from .exceptions import InvalidAPIKey


class APIKeyAuthService:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def authorize(self, key: str) -> None:
        if key != self._api_key:
            raise InvalidAPIKey()
