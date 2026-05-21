from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from deps_tables.api.models.build_info import BuildInfoModel
from deps_tables.containers import Application

service_info_router = APIRouter(prefix="/service-info")


@service_info_router.get("/version", tags=["Service Info"], response_model=BuildInfoModel)
@inject
def get_build_info(build_info=Depends(Provide[Application.core.build_info])):
    return BuildInfoModel(**build_info)
