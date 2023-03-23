import datetime
from urllib.request import Request

from src.common.consts import MessageConsts
from src.common.responses.exceptions import BaseExceptionResponse
from src.modules.auth.consts import AuthConsts
from src.modules.auth.jwt_utils import JWTUtils
from src.modules.auth.repositories import UserRepo
from src.modules.users.entities import User
from src.modules.users.entities.users import RoleEnum


class LoginService:
    def __init__(self):
        self.user_repo = UserRepo

    @classmethod
    def generate_jwt_token(cls, user: User):
        now = datetime.datetime.utcnow()
        exp = (now + datetime.timedelta(seconds=AuthConsts.TOKEN_EXPIRE_TIME)).timestamp()
        data = {
            "userName": user[User.userName.name],
            "exp": exp,
            "roleCode": AuthConsts.ROLE_CODE[user[User.role.name]]
        }
        return JWTUtils.encode(payload=data)

