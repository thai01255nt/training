from typing import Annotated, Optional

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
from src.modules.clients.dtos.clients import AddUserClientPayloadDTO, GetManagementPayloadDTO, GetPortfolioPayloadDTO
from src.modules.clients.entities import UserClientMembership
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


@client_router.post(
    "/management/management",
    dependencies=[
        Depends(authentication)
    ],
)
def get_management_by_broker_name(current_user: Annotated[TokenPayloadDTO, Depends(authentication)], payload: GetManagementPayloadDTO):
    if current_user["roleCode"] != AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value] and current_user["adminNameBroker"] != payload.brokerName:
        if current_user["adminNameBroker"] is None:
            raise BaseExceptionResponse(status_code=403, http_code=403, message=MessageConsts.FORBIDDEN)
        if current_user["adminNameBroker"] != payload.brokerName:
            response = PaginationResponse(
                http_code=200,
                status_code=200,
                message=MessageConsts.SUCCESS,
                data={"schema": [], "records": []},
                page=payload.page,
                page_size=payload.pageSize,
                total=0,
            )
            return JSONResponse(status_code=response.http_code, content=response.to_dict())

    data, total = CLIENT_SERVICE.get_management_by_broker_name(
        broker_name=payload.brokerName, page=payload.page, pageSize=payload.pageSize, filter_by=payload.filterBy.dict(exclude_unset=True), sort_by=[s.dict(exclude_unset=True) for s in payload.sortBy]
    )
    response = PaginationResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
        data=data,
        page=payload.page,
        page_size=payload.pageSize,
        total=total,
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())


@client_router.post(
    "/management/portfolio",
    dependencies=[
        Depends(authentication)
    ],
)
def get_portfolio_by_broker_name(current_user: Annotated[TokenPayloadDTO, Depends(authentication)], payload: GetPortfolioPayloadDTO):
    if current_user["roleCode"] != AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value] and current_user["adminNameBroker"] != payload.brokerName:
        if current_user["adminNameBroker"] is None:
            raise BaseExceptionResponse(status_code=403, http_code=403, message=MessageConsts.FORBIDDEN)
        if current_user["adminNameBroker"] != payload.brokerName:
            response = SuccessResponse(
                http_code=200,
                status_code=200,
                message=MessageConsts.SUCCESS,
                data={"schema": [], "records": []},
            )
            return JSONResponse(status_code=response.http_code, content=response.to_dict())
    data = CLIENT_SERVICE.get_portfolio_by_broker_name(
        broker_name=payload.brokerName, filter_by=payload.filterBy.dict(exclude_unset=True))
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
def pagination_client(current_user: Annotated[TokenPayloadDTO, Depends(authentication)], page: int, pageSize: int, brokerName: Optional[str] = None):
    records, total = CLIENT_SERVICE.get_client_pagination(
        current_user=current_user, page=page, pageSize=pageSize, brokerName=brokerName)
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
    records, total = CLIENT_SERVICE.get_client_pagination(
        current_user=current_user, page=0, pageSize=1, id_client=id_client, brokerName=None)
    if total == 0:
        raise BaseExceptionResponse(http_code=404, status_code=404, message=MessageConsts.NOT_FOUND)
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
def get_user_client(user_id: int):
    USER_SERVICE.get_by_id(user_id)
    clients = USER_CLIENT_SERVICE.user_client_membership_repo.get_membership_by_user_id(user_id=user_id)
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
        data=DataUtils.serialize_objects(clients),
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())


@user_client_router.delete(
    "/users/{user_id}/clients/{id_client}",
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ]
)
def get_user_client(user_id: int, id_client: str):
    record = USER_CLIENT_SERVICE.get_user_client(user_id=user_id, id_client=id_client)
    USER_CLIENT_SERVICE.user_client_membership_repo.delete_by_id(id=record[UserClientMembership.id.name])
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())
