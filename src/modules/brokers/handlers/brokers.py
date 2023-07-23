from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.common.consts import MessageConsts
from src.common.responses import SuccessResponse
from src.modules.auth.consts import AuthConsts
from src.modules.auth.dependencies import authentication, RoleCodePermission
from src.modules.brokers.services.brokers import BrokerService
from src.modules.users.dtos import UserResponseDTO
from src.modules.users.entities.users import RoleEnum
from src.utils.data_utils import DataUtils

broker_router = APIRouter()
BROKER_SERVICE = BrokerService()


@broker_router.get(
    "/",
    response_model=UserResponseDTO,
    dependencies=[
        Depends(authentication),
        Depends(
            RoleCodePermission(required_role_codes=[AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]])
        )
    ]
)
def get_all():
    records = BROKER_SERVICE.get_all()
    response = SuccessResponse(
        http_code=200,
        status_code=200,
        message=MessageConsts.SUCCESS,
        data=DataUtils.serialize_objects(records)
    )
    return JSONResponse(status_code=response.http_code, content=response.to_dict())
