import os
import jwt
from typing import Dict, Tuple, Optional

from src.modules.auth.consts import AuthConsts


class JWTUtils:

    @classmethod
    def encode(cls, payload):
        return jwt.encode(payload, AuthConsts.JWT_SECRET, algorithm=AuthConsts.JWT_ALGO)

    @staticmethod
    def decode_jwt_token(encode_string: str) -> Tuple[bool, Optional[Dict]]:
        try:
            result = jwt.decode(encode_string, AuthConsts.JWT_SECRET, algorithms=AuthConsts.JWT_ALGO)
        except Exception:
            return False, None
        return True, result
