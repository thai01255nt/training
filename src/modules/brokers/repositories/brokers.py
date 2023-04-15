from src.db.sessions import backend_session_scope
from src.modules.base.query_builder import BaseQueryBuilder
from src.modules.base.repositories import BaseRepo
from src.modules.brokers.entities import Broker


class BrokerRepo(BaseRepo):
    entity = Broker
    query_builder = BaseQueryBuilder(entity=entity)
    session_scope = backend_session_scope

