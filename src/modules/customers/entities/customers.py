import sqlalchemy
from sqlalchemy import text

from src.common.consts import DatabaseConsts
from src.modules.base_entities import Base


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = (
        {"schema": DatabaseConsts.SCHEMA},
    )

    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR())
    phone = sqlalchemy.Column(sqlalchemy.VARCHAR())
    createdAt = sqlalchemy.Column(sqlalchemy.DateTime)
    updatedAt = sqlalchemy.Column(sqlalchemy.DateTime, default=text(f"SWITCHOFFSET(SYSUTCDATETIME(), '+07:00')"))
