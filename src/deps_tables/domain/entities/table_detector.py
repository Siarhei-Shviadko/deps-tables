from typing import Any, List, Type

from pydantic import BaseModel


class TableDetectorInitSettings(BaseModel):
    detector_cls: Type[Any]
    detector_args: List[Any]
