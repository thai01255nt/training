from fastapi.responses import JSONResponse

from src.common.consts import MessageConsts
from src.common.responses import SuccessResponse
from src.common.responses.exceptions import BaseExceptionResponse
from src.modules.auth.dtos import LoginResponseDTO, LoginPayloadDTO
from src.modules.auth.router import auth_router
from src.modules.auth.services import LoginService
from src.utils.security import Security

LOGIN_SERVICE = LoginService()


@auth_router.post("/login", response_model=LoginResponseDTO)
def login_user(payload: LoginPayloadDTO):
    user = LOGIN_SERVICE.get_by_username(username=payload.userName)
    encrypted_password = Security.encrypt(string=payload.password)
    if encrypted_password == user.password:
        response = SuccessResponse(http_code=200, status_code=200, message=MessageConsts.SUCCESS)
        return JSONResponse(status_code=response.http_code, content=response.to_dict())
    raise BaseExceptionResponse(
        http_code=400, status_code=400, message=MessageConsts.BAD_REQUEST, errors={"password": ["password incorrect"]}
    )
