import math
from typing import List, TypeVar, Generic

import numpy as np
import pandas as pd
from sqlalchemy import select, text, values, update, delete
from sqlalchemy.sql import Values
from sqlalchemy.sql.elements import BinaryExpression

from backend.db.backend_mssql_connector import backend_session_scope as session_scope
from backend.modules.entities.entities.base_entities import Base
from backend.utils.data_utils import DataUtils

T = TypeVar("T")


class BaseRepo(Generic[T]):
    entity: T = None

    @classmethod
    def get_by_id(cls, id) -> T:
        records = cls.get_by_condition(cls.entity.id == id)
        if len(records) == 0:
            return None
        return records[0]

    @classmethod
    def get_all(cls) -> List[T]:
        return cls.get_by_condition(conditions=None)

    @classmethod
    def get_by_condition(cls, conditions) -> List[T]:
        with session_scope() as session:
            query = session.query(cls.entity)
            if conditions is not None:
                records = query.filter(conditions).all()
            else:
                records = query.all()
            session.expunge_all()
        return records

    @classmethod
    def insert(cls, record: Base) -> T:
        with session_scope() as session:
            session.add(record)
            session.flush()
            session.expunge_all()
        return record

    @classmethod
    def insert_many(cls, records: List[T]):
        if len(records) == 0:
            return []
        with session_scope() as session:
            session.add_all(records)
            session.flush()
            session.expunge_all()
        return records

    @classmethod
    def update(cls, record: Base) -> T:
        if record.id is None:
            raise Exception("constrain id when update is NOT NULL")
        database_dict = DataUtils.object_to_database_dict(entity=cls.entity, obj=record)
        database_dict.pop("id")
        sql = update(cls.entity).values(database_dict).where(record.id == cls.entity.id).returning(cls.entity)
        with session_scope() as session:
            result = session.execute(sql).fetchall()
        return cls.entity(**result[0])
