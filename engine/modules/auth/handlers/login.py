from fastapi import APIRouter
from fastapi.responses import JSONResponse

from engine.common.consts import MessageConsts
from engine.common.responses import SuccessResponse
from engine.common.responses.exceptions import BaseExceptionResponse
from engine.modules.auth.dtos import LoginResponseDTO, LoginPayloadDTO
from engine.modules.auth.services import LoginService
from engine.modules.users.entities import User
from engine.modules.users.services import UserService
from engine.utils.security import Security

auth_router = APIRouter()
LOGIN_SERVICE = LoginService()
USER_SERVICE = UserService()


@auth_router.post("/login", response_model=LoginResponseDTO)
def login_user(payload: LoginPayloadDTO):
    user = USER_SERVICE.get_by_username(username=payload.userName)
    decrypted_password = Security.decrypt(user[User.password.name])
    if decrypted_password == payload.password:
        token = LOGIN_SERVICE.generate_jwt_token(user=user)
        response = SuccessResponse(http_code=200, status_code=200, message=MessageConsts.SUCCESS, data={"token": token})
        return JSONResponse(status_code=response.http_code, content=response.to_dict())
    raise BaseExceptionResponse(
        http_code=400, status_code=400, message=MessageConsts.BAD_REQUEST, errors={"password": ["password incorrect"]}
    )
