from typing import Annotated
from fastapi import Request, Depends
from fastapi.security import HTTPBearer

from src.common.consts import MessageConsts
from src.common.responses.exceptions import BaseExceptionResponse
from src.modules.auth.consts import AuthConsts
from src.modules.auth.dtos import TokenPayloadDTO
from src.modules.auth.jwt_utils import JWTUtils
from src.modules.users.repositories import UserRepo
from src.modules.users.entities import User
from src.modules.users.entities.users import RoleEnum


class Authentication(HTTPBearer):
    async def __call__(self, request: Request):
        token = request.headers.get("Authorization", None)
        if token is None:
            raise BaseExceptionResponse(
                http_code=401,
                status_code=401,
                message=MessageConsts.UNAUTHORIZED,
                errors={"token": ["missing token in headers"]}
            )
        token = token[len("bearer "):]
        is_success, payload = JWTUtils.decode_jwt_token(encode_string=token)
        if not is_success:
            raise BaseExceptionResponse(http_code=403, status_code=403, message="Invalid token")
        if payload['roleCode'] == AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]:
            user = UserRepo.get_by_username(username=payload['userName'])
            if user[0][User.role.name] != RoleEnum.ADMIN.value:
                raise BaseExceptionResponse(http_code=403, status_code=403, message="fake admin role")
        return payload


authentication = Authentication()


class RoleCodePermission:

    def __init__(self, required_role_codes: list[str]) -> None:
        self.required_role_codes = required_role_codes

    async def __call__(self, jwt_payload: Annotated[TokenPayloadDTO, Depends(authentication)]) -> bool:
        if jwt_payload['roleCode'] not in self.required_role_codes:
            raise BaseExceptionResponse(http_code=403, status_code=403, message=MessageConsts.FORBIDDEN)
        return True
