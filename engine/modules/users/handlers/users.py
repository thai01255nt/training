from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from engine.common.consts import MessageConsts
from engine.common.responses import SuccessResponse
from engine.modules.auth.consts import AuthConsts
from engine.modules.auth.dependencies import authentication, RoleCodePermission
from engine.modules.users.dtos import UserResponseDTO, AddUserPayloadDTO
from engine.modules.users.entities import User
from engine.modules.users.entities.users import RoleEnum
from engine.modules.users.services import UserService
from engine.utils.data_utils import DataUtils

user_router = APIRouter()
USER_SERVICE = UserService()


@user_router.post(
    "/",
    response_model=UserResponseDTO,
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
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
