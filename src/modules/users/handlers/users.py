from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.common.consts import MessageConsts
from src.common.responses import SuccessResponse
from src.common.responses.pagination import PaginationResponse
from src.modules.auth.consts import AuthConsts
from src.modules.auth.dependencies import authentication, RoleCodePermission
from src.modules.auth.dtos.login import TokenPayloadDTO
from src.modules.users.dtos import UserResponseDTO, AddUserPayloadDTO
from src.modules.users.dtos.users import AdminEditUserPayloadDTO, ResetPasswordPayloadDTO
from src.modules.users.entities import User
from src.modules.users.entities.users import RoleEnum
from src.modules.users.services import UserService
from src.utils.data_utils import DataUtils
from src.utils.security import Security

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

@user_router.get(
    "/",
    # response_model=UserResponseDTO,
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ]
)
def pagination_user(page:int, pageSize:int):
    records, total = USER_SERVICE.get_user_pagination(page=page, pageSize=pageSize)
    for record in records:
        record[User.password.name] = Security.decrypt(record[User.password.name])
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

@user_router.get(
    "/{userID}",
    # response_model=UserResponseDTO,
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ]
)
def get_by_id(userID:int):
    record = USER_SERVICE.get_by_id(id=userID)
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
        data=DataUtils.serialize_object(record, exclude=["password"]),
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())

@user_router.put(
    "/resetPassword",
    # response_model=UserResponseDTO,
    dependencies=[
        Depends(authentication),
    ],
)
def reset_password(current_user: Annotated[TokenPayloadDTO, Depends(authentication)], payload: ResetPasswordPayloadDTO):
    USER_SERVICE.reset_password(current_user=current_user, payload=payload)
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())

@user_router.put(
    "/",
    # response_model=UserResponseDTO,
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ],
)
def edit_user(payload: AdminEditUserPayloadDTO):
    USER_SERVICE.edit_user(payload=payload)
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())

@user_router.delete(
    "/{userID}",
    # response_model=UserResponseDTO,
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ],
)
def delete_user(userID: int):
    USER_SERVICE.delete_user(userID=userID)
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())
