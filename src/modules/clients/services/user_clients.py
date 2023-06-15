import numpy as np
import pandas as pd
from src.common.consts import MessageConsts
from src.common.responses.exceptions import BaseExceptionResponse
from src.modules.auth.dtos import TokenPayloadDTO
from src.modules.brokers.repositories import BrokerRepo
from src.modules.clients.dtos.clients import AddUserClientPayloadDTO
from src.modules.clients.repositories import ClientRepo, UserClientMembershipRepo
from src.modules.users.repositories import UserRepo


class UserClientService:
    def __init__(self):
        self.client_repo = ClientRepo
        self.user_repo = UserRepo
        self.user_client_membership_repo = UserClientMembershipRepo

    def add_user_client(self, payload: AddUserClientPayloadDTO):
        records = self.user_repo.get_by_id(payload.userID)
        if len(records) ==0:
            raise BaseExceptionResponse(http_code=400, status_code=400, message=MessageConsts.BAD_REQUEST, errors={"userID": ["userID not exists"]})
        records = self.client_repo.get_by_id_client(payload.idClient)
        if len(records) ==0:
            raise BaseExceptionResponse(http_code=400, status_code=400, message=MessageConsts.BAD_REQUEST, errors={"idClient": ["idClient not exists"]})
        memberships = self.user_client_membership_repo.get_membership_by_user_id(user_id=payload.userID, id_client=payload.idClient)
        if len(memberships) > 0:
            raise BaseExceptionResponse(http_code=400, status_code=400, message=MessageConsts.BAD_REQUEST, errors={"idClient": ["idClient membership is already exists"]})
        self.user_client_membership_repo.insert(payload.dict(exclude_unset=True), returning=False)
        return
