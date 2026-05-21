from pydantic import Field, validator

from deps_tables.api.models.base import ConfiguredBaseModel


class RelativeAreaModel(ConfiguredBaseModel):
    top: float = Field(..., ge=0, le=1, alias="y")
    left: float = Field(..., ge=0, le=1, alias="x")
    width: float = Field(..., ge=0, le=1, alias="w")
    height: float = Field(..., ge=0, le=1, alias="h")

    @validator("width")
    def check_horizontal_size(cls, value, values):  # noqa: N805, WPS110
        assert values["left"] + value <= 1  # noqa: S101
        return value

    @validator("height")
    def check_vertical_size(cls, value, values):  # noqa: N805, WPS110
        assert values["top"] + value <= 1  # noqa: S101
        return value


class RelativeAreaModelWithPage(RelativeAreaModel):
    page: int = Field(1, ge=1)


class RowModel(ConfiguredBaseModel):
    y: float = Field(..., ge=0, le=1)


class ColumnModel(ConfiguredBaseModel):
    x: float = Field(..., ge=0, le=1)
