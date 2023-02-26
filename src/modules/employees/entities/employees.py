import sqlalchemy
from sqlalchemy import text

from src.common.consts import DatabaseConsts
from src.modules.base_entities import Base


class Employees(Base):
    __tablename__ = "employees"
    __table_args__ = (
        {"schema": DatabaseConsts.SCHEMA},
    )

    id = sqlalchemy.Column(sqlalchemy.INT)
    identityNumber = sqlalchemy.Column(sqlalchemy.VARCHAR())
    name = sqlalchemy.Column(sqlalchemy.VARCHAR())
    address = sqlalchemy.Column(sqlalchemy.VARCHAR())
    phone = sqlalchemy.Column(sqlalchemy.VARCHAR())
    createdAt = sqlalchemy.Column(sqlalchemy.DateTime)
    updatedAt = sqlalchemy.Column(sqlalchemy.DateTime, default=text(f"SWITCHOFFSET(SYSUTCDATETIME(), '+07:00')"))
