from typing import List, TypeVar, Generic, Dict, Union, Callable

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from engine.modules.base.entities import Base
from engine.modules.base.query_builder import BaseQueryBuilder, TextSQL

T = TypeVar("T")


class BaseRepo(Generic[T]):
    entity: Base = None
    query_builder: BaseQueryBuilder = None
    session_scope: Callable[..., Session] = None

    @classmethod
    def row_factory(cls, cur) -> List[T]:
        if cur.description is None:
            return []
        columns = [column[0] for column in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    @classmethod
    def insert_many(cls, records: List[Dict], returning):
        with cls.session_scope() as session:
            insert_query = cls.query_builder.insert_many(records=records, returning=returning)
            cur = session.connection().exec_driver_sql(insert_query.sql, tuple(insert_query.params)).cursor
            return cls.row_factory(cur=cur)

    @classmethod
    def insert(cls, record: Dict, returning) -> T:
        results = cls.insert_many(records=[record], returning=returning)
        if returning:
            return results[0]
        else:
            return None

    @classmethod
    def update_many(
            cls, records: List[Dict], identity_columns: List[str], returning, text_clauses: Dict[str, TextSQL] = None
    ):
        if len(identity_columns) == 0:
            raise Exception("missing require identity columns")
        with cls.session_scope() as session:
            query_values = cls.query_builder.generate_values(records=records, text_clauses=text_clauses)
            update_columns = query_values.columns.copy()
            for col in identity_columns:
                update_columns.remove(col)
            sql_set_columns = ", ".join([f"t.[{col}] = s.[{col}]" for col in update_columns])
            sql_select_columns = ", ".join(f"[{col}]" for col in query_values.columns)
            sql_conditions = " AND ".join([f"t.[{col}] = s.[{col}]" for col in identity_columns])
            sql_returning = "OUTPUT INSERTED.*" if returning else ""
            sql = f"""
                UPDATE t
                SET {sql_set_columns}
                {sql_returning}
                FROM (
                    SELECT *
                    from (
                        {query_values.sql}
                    ) _ ({sql_select_columns})
                ) s
                inner join [{cls.entity.__table__.schema}].[{cls.entity.__tablename__}] t on {sql_conditions}
            """
            cur = session.connection().exec_driver_sql(sql, tuple(query_values.params)).cursor
            results = cls.row_factory(cur=cur)
        return results

    @classmethod
    def update(cls, record: Dict, identity_columns: List[str], returning, text_clauses: Dict[str, TextSQL] = None) -> T:
        results = cls.update_many(
            records=[record], identity_columns=identity_columns, returning=returning, text_clauses=text_clauses
        )
        if returning:
            return results[0]
        else:
            return None

    @classmethod
    def get_all(cls) -> List[T]:
        with cls.session_scope() as session:
            sql = """
                SELECT *
                FROM %s
            """ % cls.query_builder.full_table_name
            cur = session.connection().exec_driver_sql(sql).cursor
            results = cls.row_factory(cur=cur)
        return results

    @classmethod
    def insert_into_temp(
            cls, records: Union[List[Dict], pd.DataFrame], temp_table: str, text_clauses: Dict[str, TextSQL] = None
    ):
        if len(records) == 0:
            return None
        records = pd.DataFrame(records).replace({np.nan: None})
        chunk_size = 1
        query_values = cls.query_builder.generate_values(records=records.iloc[:chunk_size], text_clauses=text_clauses)
        sql_columns = ", ".join(f"[{col}]" for col in query_values.columns)
        params = records.values.tolist()
        with cls.session_scope() as session:
            session.connection().exec_driver_sql(
                f"""
                    IF OBJECT_ID('tempdb..[{temp_table}]') IS NULL
                    BEGIN
                        declare @temp {cls.entity.__sqlServerType__}
                        select *
                        into [{temp_table}]
                        from @temp
                    END
                """
            )
            sql = f"""
                INSERT INTO {temp_table} ({sql_columns})
                {query_values.sql}
            """
            cur = session.connection().exec_driver_sql(sql, params).cursor
            cur.close()
        return query_values

    @classmethod
    def upsert_from_source_table(
            cls,
            source_table,
            identity_columns: List[str],
            upsert_columns: List[str],
            is_update=True,
            is_insert=True
    ):
        sql_join_conditions = " AND ".join([f"t.[{col}] = s.[{col}]" for col in identity_columns])
        # sql update
        sql_set_columns = ", ".join([f"t.[{col}] = s.[{col}]" for col in upsert_columns])
        sql_update = f"""
            UPDATE t
            SET {sql_set_columns}
            FROM {cls.entity.__table__.full_name} t
            JOIN [{source_table}] s ON {sql_join_conditions}
        """
        # sql insert
        sql_select_columns = ", ".join(f"s.[{col}]" for col in upsert_columns)
        sql_insert_columns = ", ".join(f"[{col}]" for col in upsert_columns)
        sql_insert_conditions = " or ".join([f"t.[{col}] is null" for col in identity_columns])
        sql_insert_conditions = f"""
            LEFT JOIN {cls.entity.__table__.full_name} t ON {sql_join_conditions}
            WHERE {sql_insert_conditions}
        """ if identity_columns else ""
        sql_insert = f"""
            INSERT INTO {cls.entity.__table__.full_name} ({sql_insert_columns})
            SELECT {sql_select_columns}
            FROM [{source_table}] s
            {sql_insert_conditions}
        """
        list_sql = [sql_update] if is_update and len(identity_columns) != 0 else []
        if is_insert:
            list_sql += [sql_insert]
        sql = ";\n".join(list_sql)
        with cls.session_scope() as session:
            session.connection().exec_driver_sql(sql)
        return

    @classmethod
    def get_by_id(cls, _id: int):
        condition_query = cls.query_builder.where({cls.entity.id: _id})
        sql = """
            SELECT *
            FROM
            %s
            WHERE %s
        """ % (cls.query_builder.full_table_name, condition_query.sql)
        with cls.session_scope() as session:
            cur = session.connection().exec_driver_sql(sql, condition_query.params).cursor
            records = cls.row_factory(cur=cur)
            return records
