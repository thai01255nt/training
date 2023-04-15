from src.modules.users.dtos import AddUserPayloadDTO
from src.modules.users.services import UserService

UserService().add_user(payload=AddUserPayloadDTO(userName="vukhanh1202@gmail.com",password="123456a@"))