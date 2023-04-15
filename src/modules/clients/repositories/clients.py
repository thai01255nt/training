from src.db.sessions import backend_session_scope
from src.modules.base.query_builder import BaseQueryBuilder
from src.modules.base.repositories import BaseRepo
from src.modules.clients.entities import Client


class ClientRepo(BaseRepo):
    entity = Client
    query_builder = BaseQueryBuilder(entity=entity)
    session_scope = backend_session_scope
