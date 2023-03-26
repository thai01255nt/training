import sqlalchemy

from src.common.consts import SQLServerConsts
from src.modules.base.entities import Base


class Client(Base):
    __tablename__ = "clients"
    __table_args__ = (
        {"schema": SQLServerConsts.SCHEMA},
    )

    id = sqlalchemy.Column(sqlalchemy.VARCHAR, primary_key=True)
    brokerID = sqlalchemy.Column(sqlalchemy.BIGINT)
    owner = sqlalchemy.Column(sqlalchemy.VARCHAR)
    fee = sqlalchemy.Column(sqlalchemy.FLOAT)
    createdAt = sqlalchemy.Column(sqlalchemy.DATETIME)
    updatedAt = sqlalchemy.Column(sqlalchemy.DATETIME)
