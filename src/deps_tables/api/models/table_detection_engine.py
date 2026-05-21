from pydantic import BaseModel

from deps_tables.domain.constants import TableDetectionEngineEnum


class TableDetectionEngineModel(BaseModel):
    code: TableDetectionEngineEnum
    name: str

    class Config:
        orm_mode = True
