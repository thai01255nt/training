from engine.modules.users.entities.users import RoleEnum
from engine.utils.security import Security


class AuthConsts:
    TOKEN_EXPIRE_TIME = 86400
    JWT_ALGO = "HS256"
    JWT_SECRET = Security.KEY
    ROLE_CODE = {
        RoleEnum.ADMIN.value: 1582,
        RoleEnum.TRADER.value: 1,
    }
