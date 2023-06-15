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

    @classmethod
    def get_pagination(cls, page:int, pageSize:int):
        count_sql = f"""
            SELECT count(*) as total
            FROM {cls.query_builder.full_table_name}
        """
        sql = f"""
            SELECT *
            FROM {cls.query_builder.full_table_name}
            ORDER BY role, id
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY;
        """
        select_params = [page, pageSize]
        with cls.session_scope() as session:
            cur = session.connection().exec_driver_sql(count_sql).cursor
            total = cls.row_factory(cur=cur)
            cur = session.connection().exec_driver_sql(sql, parameters=tuple(select_params)).cursor
            records = cls.row_factory(cur=cur)
            return records, total[0]["total"]
