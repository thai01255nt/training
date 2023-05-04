import sqlalchemy

from src.common.consts import SQLServerConsts
from src.modules.base.entities import Base


class Client(Base):
    __tablename__ = "client"
    __table_args__ = (
        {"schema": SQLServerConsts.SCHEMA},
    )

    id = sqlalchemy.Column(sqlalchemy.VARCHAR(0), primary_key=True)
    nameBroker = sqlalchemy.Column(sqlalchemy.VARCHAR(0))
    idClient = sqlalchemy.Column(sqlalchemy.VARCHAR(0))
    nameClient = sqlalchemy.Column(sqlalchemy.FLOAT)
    interestRate = sqlalchemy.Column(sqlalchemy.FLOAT)
    costBuy = sqlalchemy.Column(sqlalchemy.FLOAT)
    costSell = sqlalchemy.Column(sqlalchemy.FLOAT)
