import os
import jwt
from typing import Dict, Tuple, Optional, Union

from engine.modules.auth.consts import AuthConsts
from engine.modules.auth.dtos import TokenPayloadDTO


class JWTUtils:

    @classmethod
    def encode(cls, payload: TokenPayloadDTO):
        return jwt.encode(payload, AuthConsts.JWT_SECRET, algorithm=AuthConsts.JWT_ALGO)

    @staticmethod
    def decode_jwt_token(encode_string: str) -> Tuple[bool, TokenPayloadDTO]:
        try:
            result = jwt.decode(encode_string, AuthConsts.JWT_SECRET, algorithms=AuthConsts.JWT_ALGO)
        except Exception:
            return False, TokenPayloadDTO()
        return True, result
