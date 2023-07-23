from src.modules.brokers.repositories import BrokerRepo


class BrokerService:
    def __init__(self):
        self.broker_repo = BrokerRepo

    def get_all(self):
        return self.broker_repo.get_all()
