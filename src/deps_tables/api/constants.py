from deps_tables.domain.constants import TableDetectionEngineEnum

DETECTION_ENGINE_NAMES = {  # noqa: WPS407
    TableDetectionEngineEnum.AWS_TEXTRACT: "Amazon Textract",
    TableDetectionEngineEnum.AZURE_FORM_RECOGNIZER: "Azure Form Recognizer",
    TableDetectionEngineEnum.DEPS_DETECTOR: "DEPS Detector",
}

FREE_DETECTION_ENGINES = (TableDetectionEngineEnum.DEPS_DETECTOR,)
