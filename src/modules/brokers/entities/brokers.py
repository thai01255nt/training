import sqlalchemy

from src.common.consts import SQLServerConsts
from src.modules.base.entities import Base


class Broker(Base):
    __tablename__ = "broker"
    __table_args__ = (
        {"schema": SQLServerConsts.SCHEMA},
    )

    id = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    nameBroker = sqlalchemy.Column(sqlalchemy.VARCHAR(0))
    typeBroker = sqlalchemy.Column(sqlalchemy.VARCHAR(0))
    createdAt = sqlalchemy.Column(sqlalchemy.DATETIME)
    updatedAt = sqlalchemy.Column(sqlalchemy.DATETIME)
