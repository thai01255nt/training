import sqlalchemy
from sqlalchemy import text

from src.common.consts import DatabaseConsts
from src.modules.base_entities import Base


class Bill(Base):
    __tablename__ = "bills"
    __table_args__ = (
        {"schema": DatabaseConsts.SCHEMA},
    )

    id = sqlalchemy.Column(sqlalchemy.INT)
    soldDate = sqlalchemy.Column(sqlalchemy.DATE)
    customerID = sqlalchemy.Column(sqlalchemy.INT)
    employeeID = sqlalchemy.Column(sqlalchemy.INT)
    createdAt = sqlalchemy.Column(sqlalchemy.DateTime)
    updatedAt = sqlalchemy.Column(sqlalchemy.DateTime, default=text(f"SWITCHOFFSET(SYSUTCDATETIME(), '+07:00')"))
