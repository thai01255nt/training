import sqlalchemy
from sqlalchemy import text

from src.common.consts import DatabaseConsts
from src.modules.base_entities import Base


class Drug(Base):
    __tablename__ = "drugs"
    __table_args__ = (
        {"schema": DatabaseConsts.SCHEMA},
    )

    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR())
    description = sqlalchemy.Column(sqlalchemy.VARCHAR())
    mfgDate = sqlalchemy.Column(sqlalchemy.DATE)
    expDate = sqlalchemy.Column(sqlalchemy.DATE)
    createdAt = sqlalchemy.Column(sqlalchemy.DateTime)
    updatedAt = sqlalchemy.Column(sqlalchemy.DateTime, default=text(f"SWITCHOFFSET(SYSUTCDATETIME(), '+07:00')"))
