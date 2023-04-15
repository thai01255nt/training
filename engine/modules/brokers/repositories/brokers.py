from engine.db.sessions import backend_session_scope
from engine.modules.base.query_builder import BaseQueryBuilder
from engine.modules.base.repositories import BaseRepo
from engine.modules.brokers.entities import Broker


class BrokerRepo(BaseRepo):
    entity = Broker
    query_builder = BaseQueryBuilder(entity=entity)
    session_scope = backend_session_scope

