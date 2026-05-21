from enum import IntEnum

from pydantic import BaseModel


class RotationEnum(IntEnum):
    clockwise = 90
    counterclockwise = -90
    rotate_180 = 180  # noqa: WPS114


class TransformationSchema(BaseModel):
    rotation: RotationEnum
