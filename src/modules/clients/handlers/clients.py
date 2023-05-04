from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.common.consts import MessageConsts
from src.common.responses import SuccessResponse
from src.common.responses.pagination import PaginationResponse
from src.modules.auth.dependencies import authentication
from src.modules.auth.dtos import TokenPayloadDTO
from src.modules.clients.dtos import ClientResponseDTO, AddClientPayloadDTO
from src.modules.clients.services import ClientService
from src.modules.users.services import UserService
from src.utils.data_utils import DataUtils

client_router = APIRouter()
CLIENT_SERVICE = ClientService()
USER_SERVICE = UserService()


# @client_router.post(
#     "/",
#     response_model=ClientResponseDTO,
#     dependencies=[
#         Depends(authentication),
#     ]
# )
# def add_client(payload: AddClientPayloadDTO, current_user: Annotated[TokenPayloadDTO, Depends(authentication)]):
#     user = USER_SERVICE.get_by_email(email=current_user['email'])[0]
#     record = CLIENT_SERVICE.add_client(current_user=user, payload=payload)
#     response = SuccessResponse(
#         http_code=201,
#         status_code=201,
#         message=MessageConsts.CREATED,
#         data=DataUtils.serialize_object(record)
#     )
#     return JSONResponse(status_code=response.http_code, content=response.to_dict())


@client_router.get(
    "/",
    response_model=ClientResponseDTO,
    dependencies=[
        Depends(authentication),
    ],
)
def get_client(current_user: Annotated[TokenPayloadDTO, Depends(authentication)], page: int = 0, pageSize: int = 10):
    records, total = CLIENT_SERVICE.get_client_pagination(current_user=current_user, page=page, pageSize=pageSize)
    response = PaginationResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
        data=DataUtils.serialize_objects(records),
        page=page,
        page_size=pageSize,
        total=total,
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())
