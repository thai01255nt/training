from enum import Enum

import sqlalchemy

from src.common.consts import SQLServerConsts
from src.modules.base.entities import Base


class UCMRoleEnum(Enum):
    ADMIN = "admin"
    MEMBER = "member"


class UserClientMembership(Base):
    __tablename__ = "userClientMemberships"
    __table_args__ = (
        {"schema": SQLServerConsts.SCHEMA},
    )

    id = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    userID = sqlalchemy.Column(sqlalchemy.BIGINT)
    idClient = sqlalchemy.Column(sqlalchemy.VARCHAR(0))
    role = sqlalchemy.Column(sqlalchemy.VARCHAR(0))
    createdAt = sqlalchemy.Column(sqlalchemy.DATETIME)
    updatedAt = sqlalchemy.Column(sqlalchemy.DATETIME)
