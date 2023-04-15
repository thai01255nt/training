from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from engine.common.consts import MessageConsts
from engine.common.responses import SuccessResponse
from engine.modules.auth.dependencies import authentication
from engine.modules.auth.dtos import TokenPayloadDTO
from engine.modules.clients.dtos import ClientResponseDTO, AddClientPayloadDTO
from engine.modules.clients.services import ClientService
from engine.modules.users.services import UserService
from engine.utils.data_utils import DataUtils

client_router = APIRouter()
CLIENT_SERVICE = ClientService()
USER_SERVICE = UserService()


@client_router.post(
    "/",
    response_model=ClientResponseDTO,
    dependencies=[
        Depends(authentication),
    ]
)
def add_client(payload: AddClientPayloadDTO, current_user: Annotated[TokenPayloadDTO, Depends(authentication)]):
    user = USER_SERVICE.get_by_username(username=current_user['userName'])[0]
    record = CLIENT_SERVICE.add_client(user=user, payload=payload)
    response = SuccessResponse(
        http_code=201,
        status_code=201,
        message=MessageConsts.CREATED,
        data=DataUtils.serialize_object(record)
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())
