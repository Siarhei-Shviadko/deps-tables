import io
from dataclasses import field
from typing import Any, Dict, List, Optional

from ..drivers.auth_driver import AuthDriverMixin
from ..ocr import TextLine
from ..ocr.exceptions import OCREngineNotFoundError, OCRError


class OCRControllerService(AuthDriverMixin):
    def __init__(self, ocr_service_url: str, access_token: Optional[str] = None):
        self._ocr_api_url = ocr_service_url
        super().__init__(access_token=access_token)

    def extract_text(
        self,
        image: io.BytesIO,
        ocr_engine: str = "TESSERACT",
        language: Optional[str] = "eng",
        engine_settings: Dict[str, Any] = field(default_factory=dict),
    ) -> List[TextLine]:
        image.seek(0)
        files = {"file": image}
        params = {
            "engine": ocr_engine,
            "language": language,
            "engine_settings": engine_settings,
        }
        response = self._session.post(self._ocr_api_url, params=params, files=files)

        if response.status_code != 200:  # noqa: WPS432
            self._raise_exception(response.status_code, ocr_engine)

        return [TextLine(**line) for line in response.json()]

    @staticmethod
    def _raise_exception(status_code: int, engine: str) -> None:
        if status_code in (404, 422):  # noqa: WPS510
            raise OCREngineNotFoundError(f"OCR engine `{engine}` is not enabled")

        raise OCRError(f"OCR error (engine is `{engine}`)")
