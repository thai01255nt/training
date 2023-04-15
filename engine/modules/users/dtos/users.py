import datetime
from typing import TypedDict, Optional

from pydantic import validator

from engine.modules.base.dto import BaseDTO
from engine.utils.validator import Validator


class AddUserPayloadDTO(BaseDTO):
    userName: str
    password: str
    adminBrokerID: Optional[int]

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


class UserResponseDTO(TypedDict):
    id: int
    userName: str
    role: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
