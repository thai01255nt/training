from typing import Dict

from engine.db.sessions import backend_session_scope
from engine.modules.base.query_builder import BaseQueryBuilder
from engine.modules.base.repositories import BaseRepo
from engine.modules.clients.entities import UserClientMembership, UCMRoleEnum, Client
from engine.modules.clients.repositories import ClientRepo
from engine.modules.users.entities.users import RoleEnum, User
from engine.modules.users.repositories import UserRepo


class UserClientMembershipRepo(BaseRepo):
    entity = UserClientMembership
    query_builder = BaseQueryBuilder(entity=entity)
    session_scope = backend_session_scope

    @classmethod
    def add_admin_membership(cls, user: Dict, client: Dict):
        sql = f"""
            INSERT INTO {cls.query_builder.full_table_name} (userID, clientID, role)
            SELECT *
            FROM (
                SELECT
                    u.id AS userID
                    , '{client[Client.id.name]}' AS clientID
                    , CASE WHEN u.role = '{RoleEnum.ADMIN.value}'
                        THEN '{UCMRoleEnum.ADMIN.value}'
                        ELSE THEN '{UCMRoleEnum.MEMBER.value}'
                        AS role
                FROM {UserRepo.query_builder.full_table_name} u
                WHERE u.adminBrokerID = ? and u.id != ?
            ) _
        """
        with cls.session_scope() as session:
            session.connection().exec_driver_sql(sql, parameters=[client[Client.brokerID.name], user[User.id.name]])
        return
