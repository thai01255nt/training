from src.utils.security import Security


class AuthConsts:
    TOKEN_EXPIRE_TIME = 86400
    JWT_ALGO = "HS256"
    JWT_SECRET = Security.KEY
