from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.common.consts import MessageConsts
from src.common.responses import SuccessResponse
from src.modules.auth.dependencies import authentication
from src.modules.clients.dtos import ClientResponseDTO, AddClientPayloadDTO
from src.modules.clients.services import ClientService
from src.utils.data_utils import DataUtils

client_router = APIRouter()
CLIENT_SERVICE = ClientService()


@client_router.post(
    "/",
    response_model=ClientResponseDTO,
    dependencies=[
        Depends(authentication),
    ]
)
def add_user(payload: AddClientPayloadDTO):
    record = CLIENT_SERVICE.add_client(payload=payload)
    response = SuccessResponse(
        http_code=201,
        status_code=201,
        message=MessageConsts.CREATED,
        data=DataUtils.serialize_object(record)
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())
