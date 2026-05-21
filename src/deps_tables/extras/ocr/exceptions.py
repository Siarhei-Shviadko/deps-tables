class OCRServiceError(Exception):
    pass


class OCRError(OCRServiceError):
    pass


class OCREngineNotFoundError(OCRServiceError):
    pass
