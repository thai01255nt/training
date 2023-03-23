from typing import TypedDict

from src.modules.base.dto import BaseDTO


class LoginPayloadDTO(BaseDTO):
    userName: str
    password: str


class LoginResponseDTO(TypedDict):
    token: str
