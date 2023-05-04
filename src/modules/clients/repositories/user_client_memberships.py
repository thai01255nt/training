from typing import Dict

from src.db.sessions import backend_session_scope
from src.modules.auth.consts import AuthConsts
from src.modules.auth.dtos.login import TokenPayloadDTO
from src.modules.base.query_builder import BaseQueryBuilder
from src.modules.base.repositories import BaseRepo
from src.modules.clients.entities import UserClientMembership, UCMRoleEnum, Client
from src.modules.users.entities.users import RoleEnum, User


class UserClientMembershipRepo(BaseRepo):
    entity = UserClientMembership
    query_builder = BaseQueryBuilder(entity=entity)
    session_scope = backend_session_scope
    client_builder = BaseQueryBuilder(entity=Client)

    # @classmethod
    # def add_admin_membership(cls, user: Dict, client: Dict):
    #     sql = f"""
    #         INSERT INTO {cls.query_builder.full_table_name} (userID, clientID, role)
    #         SELECT *
    #         FROM (
    #             SELECT
    #                 u.id AS userID
    #                 , '{client[Client.id.name]}' AS clientID
    #                 , CASE WHEN u.role = '{RoleEnum.ADMIN.value}'
    #                     THEN '{UCMRoleEnum.ADMIN.value}'
    #                     ELSE THEN '{UCMRoleEnum.MEMBER.value}'
    #                     AS role
    #             FROM {UserRepo.query_builder.full_table_name} u
    #             WHERE u.adminBrokerID = ? and u.id != ?
    #         ) _
    #     """
    #     with cls.session_scope() as session:
    #         session.connection().exec_driver_sql(sql, parameters=[client[Client.brokerID.name], user[User.id.name]])
    #     return
    @classmethod
    def pagination_client_by_current_user(cls, current_user: TokenPayloadDTO, page: int, pageSize: int):
        if current_user["roleCode"] == AuthConsts.ROLE_CODE[RoleEnum.ADMIN.value]:
            select_sql = f"""
                SELECT *
                FROM {cls.client_builder.full_table_name}
                ORDER BY id
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY;
            """
            count_sql = f"""
                SELECT count(*) as total
                FROM {cls.client_builder.full_table_name}
            """
            select_params = [page * pageSize, pageSize]
            count_params = []
        else:
            params = [current_user["id"]]
            admin_brokder_sql = ""
            if current_user["adminNameBroker"] is not None:
                admin_brokder_sql = " OR c.nameBroker = ?"
                params.append(current_user["adminNameBroker"])
            select_sql = f"""
                SELECT DISTINCT c.*
                FROM {cls.client_builder.full_table_name} c
                LEFT JOIN {cls.query_builder.full_table_name} uc ON c.idClient = uc.idClient
                WHERE uc.userID = ? {admin_brokder_sql}
                ORDER BY c.id
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY;
            """
            count_sql = f"""
                SELECT count(DISTINCT c.id) as total
                FROM {cls.client_builder.full_table_name} c
                LEFT JOIN {cls.query_builder.full_table_name} uc ON c.idClient = uc.idClient
                WHERE uc.userID = ? {admin_brokder_sql}
            """
            select_params = params.copy()
            count_params = params.copy()
            select_params += [page * pageSize, pageSize]
        with cls.session_scope() as session:
            cur = session.connection().exec_driver_sql(count_sql, parameters=tuple(count_params)).cursor
            total = cls.row_factory(cur=cur)
            cur = session.connection().exec_driver_sql(select_sql, parameters=tuple(select_params)).cursor
            records = cls.row_factory(cur=cur)
            return records, total[0]["total"]
