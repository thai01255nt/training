from engine.common.consts import MessageConsts
from engine.common.responses.exceptions import BaseExceptionResponse
from engine.modules.auth.dtos import TokenPayloadDTO
from engine.modules.brokers.entities import Broker
from engine.modules.brokers.repositories import BrokerRepo
from engine.modules.clients.dtos import AddClientPayloadDTO
from engine.modules.clients.entities import UserClientMembership, Client, UCMRoleEnum
from engine.modules.clients.repositories import ClientRepo, UserClientMembershipRepo
from engine.modules.users.entities import User


class ClientService:
    def __init__(self):
        self.client_repo = ClientRepo
        self.broker_repo = BrokerRepo
        self.user_client_membership_repo = UserClientMembershipRepo

    def add_client(self, user: dict, payload: AddClientPayloadDTO):
        brokers = self.broker_repo.get_by_id(_id=payload.brokerID)
        if len(brokers) == 0:
            raise BaseExceptionResponse(
                http_code=400,
                status_code=400,
                message=MessageConsts.BAD_REQUEST,
                errors={"brokerID": ["brokerID is not exists"]}
            )
        with self.client_repo.session_scope():
            data = payload.dict()
            client = self.client_repo.insert(record=data, returning=True)
            ucm = {
                UserClientMembership.userID.name: user[User.id.name],
                UserClientMembership.clientID.name: client[Client.id.name],
                UserClientMembership.role.name: UCMRoleEnum.ADMIN.value,
            }
            self.user_client_membership_repo.insert(record=ucm, returning=False)
            self.user_client_membership_repo.add_admin_membership(client=client, user=user)
        return client
