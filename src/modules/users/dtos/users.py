import datetime
from typing import TypedDict, Optional

from pydantic import validator

from src.modules.base.dto import BaseDTO
from src.utils.validator import Validator


class AddUserPayloadDTO(BaseDTO):
    email: str
    password: str
    adminBrokerID: Optional[int]

    @validator("email", "password")
    def validate_not_none(cls, v):
        Validator.validate_not_none(value=v)
        return v

    @validator("password")
    def validate_password(cls, v: str):
        Validator.validate_password(value=v)
        return v

    @validator("email")
    def validate_email(cls, v: str):
        v = v.strip()
        Validator.validate_email(value=v)
        return v


class UserResponseDTO(TypedDict):
    id: int
    email: str
    role: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime