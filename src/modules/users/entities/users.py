from enum import Enum

import sqlalchemy

from src.common.consts import SQLServerConsts
from src.modules.base.entities import Base


class RoleEnum(Enum):
    ADMIN = "admin"
    TRADER = "trader"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        {"schema": SQLServerConsts.SCHEMA},
    )

    id = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    userName = sqlalchemy.Column(sqlalchemy.VARCHAR)
    password = sqlalchemy.Column(sqlalchemy.VARCHAR)
    role = sqlalchemy.Column(sqlalchemy.VARCHAR)
    createdAt = sqlalchemy.Column(sqlalchemy.DATETIME)
    updatedAt = sqlalchemy.Column(sqlalchemy.DATETIME)
