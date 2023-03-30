from typing import TypedDict

from pydantic import validator

from src.modules.base.dto import BaseDTO
from src.utils.validator import Validator


class LoginPayloadDTO(BaseDTO):
    userName: str
    password: str

    @validator("userName", "password")
    def validate_not_none(cls, v):
        Validator.validate_not_none(value=v)
        return v

    @validator("password")
    def validate_password(cls, v: str):
        Validator.validate_password(value=v)
        return v

    @validator("userName")
    def validate_user_name(cls, v: str):
        v = v.strip()
        Validator.validate_email(value=v)
        return v


class LoginResponseDTO(TypedDict):
    token: str


class TokenPayloadDTO(TypedDict, total=False):
    userName: str
    exp: int
    roleCode: int
    adminBrokerID: int
