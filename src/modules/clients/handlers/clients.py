from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.common.consts import MessageConsts
from src.common.responses import SuccessResponse
from src.common.responses.exceptions.base_exceptions import BaseExceptionResponse
from src.common.responses.pagination import PaginationResponse
from src.modules.auth.consts import AuthConsts
from src.modules.auth.dependencies import RoleCodePermission, authentication
from src.modules.auth.dtos import TokenPayloadDTO
from src.modules.clients.dtos import ClientResponseDTO, AddClientPayloadDTO
from src.modules.clients.dtos.clients import AddUserClientPayloadDTO
from src.modules.clients.services import ClientService, UserClientService
from src.modules.users.entities.users import RoleEnum, User
from src.modules.users.services import UserService
from src.utils.data_utils import DataUtils

client_router = APIRouter()
user_client_router = APIRouter()
CLIENT_SERVICE = ClientService()
USER_SERVICE = UserService()
USER_CLIENT_SERVICE = UserClientService()

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
    "/management/management/{broker_name}",
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ],
)
def get_management_by_broker_name(broker_name: str, page: int, pageSize: int):
    data, total = CLIENT_SERVICE.get_management_by_broker_name(broker_name=broker_name, page=page, pageSize=pageSize)
    response = PaginationResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
        data=data,
        page=page,
        page_size=pageSize,
        total=total,
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())


@client_router.get(
    "/management/portfolio/{broker_name}",
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ],
)
def get_portfolio_by_broker_name(broker_name: str):
    data = CLIENT_SERVICE.get_portfolio_by_broker_name(broker_name=broker_name)
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
        data=data,
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())


@client_router.get(
    "/",
    response_model=ClientResponseDTO,
    dependencies=[
        Depends(authentication),
    ],
)
def pagination_client(current_user: Annotated[TokenPayloadDTO, Depends(authentication)], brokerName: str, page: int, pageSize: int):
    records, total = CLIENT_SERVICE.get_client_pagination(current_user=current_user, page=page, pageSize=pageSize, brokerName=brokerName)
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


@client_router.get(
    "/{id_client}",
    response_model=ClientResponseDTO,
    dependencies=[
        Depends(authentication),
    ],
)
def get_report_by_id_client(current_user: Annotated[TokenPayloadDTO, Depends(authentication)], id_client: str):
    # records, total = CLIENT_SERVICE.get_client_pagination(
    #     current_user=current_user, page=0, pageSize=1, id_client=id_client, brokerName=None)
    # if total == 0:
    #     raise BaseExceptionResponse(http_code=404, status_code=404, message=MessageConsts.NOT_FOUND)
    results = CLIENT_SERVICE.get_report_by_id_client(id_client=id_client)
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
        data=results,
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())

@user_client_router.post(
    "/",
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ]
)
def add_user_client(payload: AddUserClientPayloadDTO):
    # records, total = CLIENT_SERVICE.get_client_pagination(
    #     current_user=current_user, page=0, pageSize=1, id_client=id_client, brokerName=None)
    # if total == 0:
    #     raise BaseExceptionResponse(http_code=404, status_code=404, message=MessageConsts.NOT_FOUND)
    USER_CLIENT_SERVICE.add_user_client(payload=payload)
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())

@user_client_router.get(
    "/users/{user_id}/clients",
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ]
)
def add_user_client(user_id: int):
    # records, total = CLIENT_SERVICE.get_client_pagination(
    #     current_user=current_user, page=0, pageSize=1, id_client=id_client, brokerName=None)
    # if total == 0:
    #     raise BaseExceptionResponse(http_code=404, status_code=404, message=MessageConsts.NOT_FOUND)
    USER_SERVICE.get_by_id(user_id)
    clients = USER_CLIENT_SERVICE.user_client_membership_repo.get_membership_by_user_id(user_id=user_id)
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
        data=DataUtils.serialize_objects(clients),
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())
