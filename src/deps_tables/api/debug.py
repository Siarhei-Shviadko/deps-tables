from fastapi import APIRouter, status

router = APIRouter()


@router.get("/debug/500", tags=["Debug"], status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
def raise_internal_server_error():
    raise ValueError()
