from typing import List

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.common.consts import MessageConsts
from src.modules.auth.handlers import auth_router
from src.modules.base.dto import BaseDTO
from src.modules.clients.handlers import client_router, user_client_router
from src.modules.users.handlers import user_router
from src.modules.brokers.handlers import broker_router


class ErrorDetailModel(BaseDTO):
    field: List[str]


class ErrorResponseModel(BaseDTO):
    statusCode: int
    message: str
    error: ErrorDetailModel


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        # 400: {"model": ErrorResponseModel},
        401: {"model": ErrorResponseModel},
        422: {"model": ErrorResponseModel},
        500: {"model": ErrorResponseModel},
    },
)

api_router.include_router(auth_router, prefix="", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(client_router, prefix="/clients", tags=["clients"])
api_router.include_router(user_client_router, prefix="/userClientMemberships", tags=["userClientMemberships"])
api_router.include_router(broker_router, prefix="/brokers", tags=["brokers"])

@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return JSONResponse(status_code=200, content={"message": MessageConsts.SUCCESS})
