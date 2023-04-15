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

    @validator("email")
    def validate_user_name(cls, v: str):
        v = v.strip()
        Validator.validate_email(value=v)
        return v


class LoginResponseDTO(TypedDict):
    token: str


class TokenPayloadDTO(TypedDict, total=False):
    email: str
    exp: int
    roleCode: int
    adminBrokerID: int
