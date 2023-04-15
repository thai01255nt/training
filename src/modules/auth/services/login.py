import datetime

from src.modules.auth.consts import AuthConsts
from src.modules.auth.dtos import TokenPayloadDTO
from src.modules.auth.jwt_utils import JWTUtils
from src.modules.users.repositories import UserRepo
from src.modules.users.entities import User
from src.utils.time_utils import TimeUtils


class LoginService:
    def __init__(self):
        self.user_repo = UserRepo

    @classmethod
    def generate_jwt_token(cls, user: dict):
        now = TimeUtils.get_current_vn_time()
        exp = int((now + datetime.timedelta(seconds=AuthConsts.TOKEN_EXPIRE_TIME)).timestamp())
        data: TokenPayloadDTO = {
            "email": user[User.email.name],
            "exp": exp,
            "roleCode": AuthConsts.ROLE_CODE[user[User.role.name]],
            "adminBrokerID": user[User.adminBrokerID.name],
        }
        return JWTUtils.encode(payload=data)
