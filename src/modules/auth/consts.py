from src.modules.users.entities.users import RoleEnum
from src.utils.security import Security


class AuthConsts:
    TOKEN_EXPIRE_TIME = 28800
    JWT_ALGO = "HS256"
    JWT_SECRET = Security.KEY
    ROLE_CODE = {
        RoleEnum.ADMIN.value: 1582,
        RoleEnum.TRADER.value: 1,
    }
