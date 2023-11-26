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
USER_SORT_FIELDS = ["email", "nameBroker"]

class UserOrderByDTO(BaseDTO):
    field: str
    direction: str

    @validator("field")
    def validate_field(cls, v):
        Validator.validate_allowed(allowed_values=USER_SORT_FIELDS, value=v)
        return v

    @validator("direction")
    def validate_direction(cls, v):
        Validator.validate_allowed(allowed_values=SORT_DIRECTIONS, value=v)
        return v
    
class UserFilterByDTO(BaseDTO):
    email: Optional[str]
    nameBroker: Optional[str]

    @validator("email")
    def validate_email(cls, v):
        return {"op": "LIKE", "value": f"%{v}%"}

    @validator("nameBroker")
    def validate_nameBroker(cls, v):
        return {"op": "LIKE", "value": f"%{v}%"}

class GetUserPayloadDTO(BaseDTO):
    sortBy: List[UserOrderByDTO] = Field(default_factory=lambda: [])
    filterBy: UserFilterByDTO = Field(default_factory=lambda: UserFilterByDTO())
    page: int
    pageSize: int

    @validator("pageSize")
    def validate_pageSize(cls, v):
        assert v > 0, "pageSize mustbe greater than zero"
        return v


class AddUserPayloadDTO(BaseDTO):
    email: str
    repeatDefaultPassword: str
    defaultPassword: str
    adminNameBroker: Optional[str]

    @validator("email", "defaultPassword", "repeatDefaultPassword")
    def validate_not_none(cls, v):
        Validator.validate_not_none(value=v)
        return v

    @validator("defaultPassword")
    def validate_default_password(cls, v: str, values):
        Validator.validate_password(value=v)
        assert v == values["repeatDefaultPassword"], "repeatPassword not match"
        return v

    @validator("email", pre=True)
    def validate_email(cls, v: str):
        v = v.strip()
        try:
            Validator.validate_email(value=v)
        except Exception as email_except:
            try:
                Validator.validate_id_client(value=v)
            except Exception as id_client_except:
                assert False, str(email_except) + " or " + str(id_client_except)
        return v


class UserResponseDTO(TypedDict):
    id: int
    email: str
    role: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime


class ResetPasswordPayloadDTO(BaseDTO):
    oldPassword: str
    repeatNewPassword: str
    newPassword: str

    @validator("newPassword")
    def validate_new_password(cls, v: str, values):
        Validator.validate_password(value=v)
        assert v == values["repeatNewPassword"], "repeatNewPassword not match"
        return v

    @validator("oldPassword")
    def validate_old_password(cls, v: str):
        Validator.validate_password(value=v)
        return v

class AdminEditUserPayloadDTO(BaseDTO):
    userID: int
    adminBrokerName: Optional[str]
    # password: Optional[str]

    # @validator("password")
    # def validate_password(cls, v: str):
    #     Validator.validate_password(value=v)
    #     return v
