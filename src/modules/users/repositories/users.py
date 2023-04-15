from sqlalchemy import select

from src.db.sessions import backend_session_scope
from src.modules.base.query_builder import BaseQueryBuilder
from src.modules.base.repositories import BaseRepo
from src.modules.users.entities import User


class UserRepo(BaseRepo):
    entity = User
    query_builder = BaseQueryBuilder(entity=entity)
    session_scope = backend_session_scope

    @classmethod
    def get_by_email(cls, email: str):
        sql = select(User).where(cls.entity.email == email)
        with cls.session_scope() as session:
            cur = session.connection().execute(sql).cursor
            return cls.row_factory(cur=cur)
