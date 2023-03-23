from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.common.consts import MessageConsts
from src.common.responses import SuccessResponse
from src.modules.auth.consts import AuthConsts
from src.modules.auth.dependencies import authentication, RolePermission
from src.modules.users.dtos import UserResponseDTO, AddUserPayloadDTO
from src.modules.users.entities import User
from src.modules.users.entities.users import RoleEnum
from src.modules.users.services import UserService
from src.utils.data_utils import DataUtils

user_router = APIRouter()
USER_SERVICE = UserService()


@user_router.post(
    "/",
    response_model=UserResponseDTO,
    dependencies=[
        Depends(authentication),
        Depends(
            RolePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ]
)
def add_user(payload: AddUserPayloadDTO):
    record = USER_SERVICE.add_user(payload=payload)
    response = SuccessResponse(
        http_code=201,
        status_code=201,
        message=MessageConsts.CREATED,
        data=DataUtils.serialize_object(record, exclude=["password"])
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())
