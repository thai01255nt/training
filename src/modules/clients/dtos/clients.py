import datetime
from typing import TypedDict, Optional

from pydantic import validator

from src.modules.base.dto import BaseDTO
from src.utils.validator import Validator


class AddClientPayloadDTO(BaseDTO):
    brokerID: int
    owner: str
    fee: float

    @validator("brokerID", "owner", "fee")
    def validate_not_none(cls, v):
        Validator.validate_not_none(value=v)
        return v

    @validator("owner")
    def validate_owner(cls, v: str):
        v = v.strip()
        Validator.validate_name(value=v)
        assert len(v) <= 64, "Must be <= 64 in length"
        return v

    @validator("fee")
    def validate_fee(cls, v):
        assert v > 0, "Must be greater than 0"
        return v


class ClientResponseDTO(TypedDict):
    id: int
    brokerID: int
    owner: str
    fee: float
    createdAt: datetime.datetime
    updatedAt: datetime.datetime


class AddUserClientPayloadDTO(BaseDTO):
    userID: int
    idClient: str

    @validator("idClient")
    def validate_id_client(cls, v: str):
        Validator.validate_id_client(value=v)
        return v
