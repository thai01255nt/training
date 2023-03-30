from src.modules.brokers.repositories import BrokerRepo


class BrokerService:
    def __init__(self):
        self.broker_repo = BrokerRepo
