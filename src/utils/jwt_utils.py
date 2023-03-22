import os
import jwt
from typing import Dict, Tuple, Optional


class JWTUtils:
    KEY = os.environ.get("ENCRYPT_KEY")

    @staticmethod
    def encode(payload: Dict) -> str:
        return jwt.encode(payload, JWTUtils.KEY)

    @staticmethod
    def decode(encode_string: str) -> Tuple[bool, Optional[Dict]]:
        try:
            result = jwt.decode(encode_string, JWTUtils.KEY, algorithms=["HS256"])
        except Exception:
            return False, None
        return True, result
