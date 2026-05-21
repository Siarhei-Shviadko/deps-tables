from pydantic import BaseModel, Field


class BuildInfoModel(BaseModel):
    build_tag: str = Field(default="", alias="buildTag")
    build_date: str = Field(default="", alias="buildDate")
    commit_hash: str = Field(default="", alias="commitHash")

    class Config:
        allow_population_by_field_name = True
