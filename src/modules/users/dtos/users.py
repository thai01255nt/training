import datetime
from typing import TypedDict

from src.modules.base.dto import BaseDTO


class AddUserPayloadDTO(BaseDTO):
    userName: str
    password: str


class UserResponseDTO(TypedDict):
    id: int
    userName: str
    role: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
