from src.modules.base.dto import BaseDto


class LoginPayloadDTO(BaseDto):
    userName: str
    password: str


class LoginResponseDTO(BaseDto):
    token: str
