import datetime

import jwt

from src.common.consts import MessageConsts
from src.common.responses.exceptions import BaseExceptionResponse
from src.modules.auth.consts import AuthConsts
from src.modules.auth.repositories import UserRepo
from src.modules.users.entities import User


class LoginService:
    def __init__(self):
        self.user_repo = UserRepo

    def get_by_username(self, username: str):
        records = self.user_repo.get_by_username(username=username)
        if len(records) == 0:
            raise BaseExceptionResponse(
                http_code=400,
                status_code=400,
                message=MessageConsts.BAD_REQUEST,
                errors={"userName": ["userName not exists"]}
            )
        return records[0]

    @classmethod
    def generate_jwt_token(cls, user: User):
        now = datetime.datetime.utcnow()
        exp = (now + datetime.timedelta(seconds=AuthConsts.TOKEN_EXPIRE_TIME)).timestamp()
        data = {
            "userName": user.userName,
            "exp": exp,
        }
        return jwt.encode(data, AuthConsts.JWT_SECRET, algorithm=AuthConsts.JWT_ALGO)
