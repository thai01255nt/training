from typing import TypedDict

from pydantic import validator

from src.modules.base.dto import BaseDTO
from src.utils.validator import Validator


class LoginPayloadDTO(BaseDTO):
    email: str
    password: str

    @validator("email", "password")
    def validate_not_none(cls, v):
        Validator.validate_not_none(value=v)
        return v

    @validator("password")
    def validate_password(cls, v: str):
        try:
            Validator.validate_password(value=v)
        except:
            assert False, "invalid password"
        return v

    @validator("email")
    def validate_user_name(cls, v: str):
        v = v.strip()
        try:
            Validator.validate_email(value=v)
        except Exception as email_except:
            try:
                Validator.validate_id_client(value=v)
            except Exception as id_client_except:
                assert False, str(email_except) + " or " + str(id_client_except)
        return v


class LoginResponseDTO(TypedDict):
    token: str


class TokenPayloadDTO(TypedDict, total=False):
    id: int
    email: str
    exp: int
    roleCode: int
    adminNameBroker: str
