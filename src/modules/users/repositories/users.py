from typing import Dict, List
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
    def get_pagination(cls, page:int, pageSize:int, filter_by: Dict, sort_by: List[Dict]):
        count_params = []
        select_params = []
        if len(sort_by) == 0:
            sort_by.append({"field": "email", "direction": "asc"})
        sort_sql = [f"""{col["field"]} {col["direction"]}""" for col in sort_by]
        sort_sql = "" if len(sort_sql) == 0 else "ORDER BY " + ", ".join(sort_sql)
        if len(filter_by) == 0:
            filter_sql = ""
        else:
            filter_sql = []
            for col in filter_by:
                filter_sql.append(f"{col} {filter_by[col]['op']} ?")
                select_params.append(filter_by[col]['value'])
                count_params.append(filter_by[col]['value'])
            filter_sql = " AND ".join(filter_sql)
            filter_sql = f"WHERE {filter_sql}"
        select_params += [page*pageSize, pageSize]
        count_sql = f"""
            SELECT count(*) as total
            FROM {cls.query_builder.full_table_name} u
            left join client c on c.idClient = u.email
            {filter_sql}
        """
        sql = f"""
            SELECT *
            from (
                select u.*, nameBroker
                FROM {cls.query_builder.full_table_name} u
                left join client c on c.idClient = u.email
            ) _
            {filter_sql}
            {sort_sql}
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY;
        """
        with cls.session_scope() as session:
            cur = session.connection().exec_driver_sql(count_sql, tuple(count_params)).cursor
            total = cls.row_factory(cur=cur)
            cur = session.connection().exec_driver_sql(sql, parameters=tuple(select_params)).cursor
            records = cls.row_factory(cur=cur)
            return records, total[0]["total"]
