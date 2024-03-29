from typing import Dict, List
from src.common.consts import MessageConsts
from src.common.responses.exceptions import BaseExceptionResponse
from src.modules.auth.dtos.login import TokenPayloadDTO
from src.modules.brokers.entities.brokers import Broker
from src.modules.brokers.repositories import BrokerRepo
from src.modules.users.dtos.users import AdminEditUserPayloadDTO, ResetPasswordPayloadDTO
from src.modules.users.repositories import UserRepo
from src.modules.users.dtos import AddUserPayloadDTO
from src.modules.users.entities.users import RoleEnum, User
from src.utils.security import Security


class UserService:
    def __init__(self):
        self.user_repo = UserRepo
        self.broker_repo = BrokerRepo

    def get_by_id(self, id: str):
        records = self.user_repo.get_by_id(id)
        if len(records) == 0:
            raise BaseExceptionResponse(
                http_code=400,
                status_code=400,
                message=MessageConsts.BAD_REQUEST,
                errors={"email": ["userID not exists"]},
            )
        return records[0]

    def get_by_email(self, email: str):
        records = self.user_repo.get_by_email(email=email)
        if len(records) == 0:
            raise BaseExceptionResponse(
                http_code=400,
                status_code=400,
                message=MessageConsts.BAD_REQUEST,
                errors={"email": ["email not exists"]},
            )
        return records[0]

    def add_user(self, payload: AddUserPayloadDTO):
        records = self.user_repo.get_by_email(email=payload.email)
        if len(records) != 0:
            raise BaseExceptionResponse(
                http_code=400, status_code=400, message=MessageConsts.BAD_REQUEST, errors={"email": ["email is exists"]}
            )
        if payload.adminNameBroker is not None:
            brokers = self.broker_repo.get_by_condition({Broker.nameBroker.name: payload.adminNameBroker})
            if len(brokers) == 0:
                raise BaseExceptionResponse(
                    http_code=400,
                    status_code=400,
                    message=MessageConsts.BAD_REQUEST,
                    errors={"adminBrokerName": ["adminBrokerName is not exists"]},
                )
        payload.defaultPassword = Security.encrypt(payload.defaultPassword)
        data = payload.dict()
        data.pop("repeatDefaultPassword", None)
        data["password"] = data.pop("defaultPassword", None)
        data[User.role.name] = RoleEnum.TRADER.value
        return self.user_repo.insert(record=data, returning=True)
    
    def get_user_pagination(self, page: int, pageSize: int, filter_by: Dict, sort_by: List[Dict]):
        return self.user_repo.get_pagination(page=page, pageSize=pageSize, filter_by=filter_by, sort_by=sort_by)

    def reset_password(self, current_user: TokenPayloadDTO, payload: ResetPasswordPayloadDTO):
        user = self.get_by_id(current_user["id"])
        if Security.decrypt(user[User.password.name]) != payload.oldPassword:
            raise BaseExceptionResponse(http_code=400, status_code=400, message=MessageConsts.BAD_REQUEST, errors={"oldPassword": ["oldPassword is incorrect"]})
        update_data = {
            "id": current_user["id"],
            "password": Security.encrypt(payload.newPassword)
        }
        self.user_repo.update(record=update_data, identity_columns=[User.id.name], returning=False)
        return

    def edit_user(self, payload: AdminEditUserPayloadDTO):
        if payload.adminBrokerName is not None:
            brokers = self.broker_repo.get_by_condition({Broker.nameBroker.name: payload.adminBrokerName})
            if len(brokers) == 0:
                raise BaseExceptionResponse(
                    http_code=400,
                    status_code=400,
                    message=MessageConsts.BAD_REQUEST,
                    errors={"adminBrokerName": ["adminBrokerName is not exists"]},
                )
        user = self.get_by_id(payload.userID)
        update_user = {
            User.id.name: user[User.id.name],
            User.adminNameBroker.name: payload.adminBrokerName,
        }
        # if payload.password is not None:
        #     update_user[User.password.name] = Security.encrypt(payload.password)
        self.user_repo.update(update_user, identity_columns=[User.id.name], returning=False)
        return

    def delete_user(self, userID: int):
        user = self.get_by_id(userID)
        self.user_repo.delete_by_id(user[User.id.name])
        return
