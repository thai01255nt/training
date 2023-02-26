import sqlalchemy
from sqlalchemy import text

from src.common.consts import DatabaseConsts
from src.modules.base_entities import Base


class BillDrug(Base):
    __tablename__ = "billDrugs"
    __table_args__ = (
        {"schema": DatabaseConsts.SCHEMA},
    )

    soldDate = sqlalchemy.Column(sqlalchemy.DATE)
    billID = sqlalchemy.Column(sqlalchemy.INT)
    drugID = sqlalchemy.Column(sqlalchemy.INT)
