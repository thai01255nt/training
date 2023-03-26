from src.modules.clients.dtos import AddClientPayloadDTO
from src.modules.clients.repositories import ClientRepo


class ClientService:
    def __init__(self):
        self.client_repo = ClientRepo

    def add_client(self, payload: AddClientPayloadDTO):
        pass
