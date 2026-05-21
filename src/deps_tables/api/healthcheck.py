from fastapi import APIRouter

healthcheck_router = APIRouter()


@healthcheck_router.get("/healthcheck", tags=["Debug"])
def service_healthcheck():
    """endpoint can be used in docker healthcheck"""
    return ""
