import datetime
from typing import List, TypedDict, Optional

from pydantic import Field, validator

from src.modules.base.dto import BaseDTO
from src.utils.validator import Validator
OPS = [
    ">",
    "<",
    ">=",
    "<=",
    "!="
]
SORT_DIRECTIONS = ["ASC", "DESC"]
MANAMENT_SORT_FIELDS = ["idClient", "nav", "totalValueSell"]

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


class PortfolioFilterByDTO(BaseDTO):
    idClient: Optional[str]
    ticker: Optional[str]

    @validator("idClient")
    def validate_idClient(cls, v):
        return {"op": "LIKE", "value": f"%{v}%"}

    @validator("ticker")
    def validate_ticker(cls, v):
        return {"op": "LIKE", "value": f"%{v}%"}


class ManagmentFilterByDTO(BaseDTO):
    idClient: Optional[str]
    depositRate: Optional[str]

    @validator("idClient")
    def validate_idClient(cls, v):
        return {"op": "LIKE", "value": f"%{v}%"}

    @validator("depositRate")
    def validate_ticker(cls, v):
        v = v.strip()
        op = v.split(" ")
        assert op[0] in OPS, f"operator should be in {OPS}"
        value = " ".join(op[1:])
        value = value.strip()
        try:
            value = float(value)
        except:
            assert False, "value must be a float value"
        op = op[0]
        return {"op": op, "value": value/100}


class ManagementOrderByDTO(BaseDTO):
    field: str
    direction: str

    @validator("field")
    def validate_field(cls, v):
        Validator.validate_allowed(allowed_values=MANAMENT_SORT_FIELDS, value=v)
        return v

    @validator("direction")
    def validate_direction(cls, v):
        Validator.validate_allowed(allowed_values=SORT_DIRECTIONS, value=v)
        return v


class GetPortfolioPayloadDTO(BaseDTO):
    brokerName: str
    filterBy: PortfolioFilterByDTO = Field(default_factory=lambda: PortfolioFilterByDTO())


class GetManagementPayloadDTO(BaseDTO):
    brokerName: str
    sortBy: List[ManagementOrderByDTO] = Field(default_factory=lambda: [])
    filterBy: ManagmentFilterByDTO = Field(default_factory=lambda: ManagmentFilterByDTO())
    page: int
    pageSize: int

    @validator("pageSize")
    def validate_pageSize(cls, v):
        assert v > 0, "pageSize mustbe greater than zero"
        return v
