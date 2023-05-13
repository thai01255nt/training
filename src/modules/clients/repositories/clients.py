import numpy as np
import pandas as pd
from src.db.sessions import backend_session_scope
from src.modules.auth.dtos.login import TokenPayloadDTO
from src.modules.base.query_builder import BaseQueryBuilder
from src.modules.base.repositories import BaseRepo
from src.modules.clients.entities import Client


class ClientRepo(BaseRepo):
    entity = Client
    query_builder = BaseQueryBuilder(entity=entity)
    session_scope = backend_session_scope

    @classmethod
    def data_frame_factory(cls, cur) -> pd.DataFrame:
        columns = [column[0] for column in cur.description]
        results = cur.fetchall()
        results = pd.DataFrame(results, columns=columns)
        return results

    @classmethod
    def get_report_by_id_client(cls, id_client: str):
        with cls.session_scope() as session:
            expected_pnl_sql = f"""
                SELECT 
                    dateBuy,
                    dateSell,
                    ticker,
                    quantity,
                    quantityAvailable,
                    priceBuy,
                    priceSell,
                    totalValueBuy,
                    totalValueSell,
                    totalValueLoan,
                    costBuy,
                    costSell,
                    nDayLoan,
                    nDayAdvance,
                    costLoanFromDayLoan,
                    costLoanFromDayAdvance,
                    costLoan,
                    pnl,
                    depositRatio,
                    minDeposit
                FROM {cls.query_builder.schema}.expected_pnl
                WHERE idClient = ?
            """
            cur = session.connection().exec_driver_sql(expected_pnl_sql, tuple([id_client])).cursor
            expected_pnl = cls.data_frame_factory(cur=cur)

            realised_pnl_sql = f"""
                SELECT
                    dateBuy,
                    dateSell,
                    ticker,
                    quantity,
                    quantityAvailable,
                    priceBuy,
                    priceSell,
                    totalValueBuy,
                    totalValueSell,
                    totalValueLoan,
                    costBuy,
                    costSell,
                    nDayLoan,
                    nDayAdvance,
                    costLoanFromDayLoan,
                    costLoanFromDayAdvance,
                    costLoan,
                    pnl,
                    depositRatio,
                    minDeposit
                FROM {cls.query_builder.schema}.realised_pnl
                WHERE idClient = ?
            """
            cur = session.connection().exec_driver_sql(realised_pnl_sql, tuple([id_client])).cursor
            realised_pnl = cls.data_frame_factory(cur=cur)

            deposit_sql = f"""
                SELECT 
                    date,
                    deposit
                FROM {cls.query_builder.schema}.deposit
                WHERE idClient = ?
            """
            cur = session.connection().exec_driver_sql(deposit_sql, tuple([id_client])).cursor
            deposit = cls.data_frame_factory(cur=cur)

            portfolio_sql = f"""
                select ticker, 
                sum(quantity) as quantity, 
                sum(quantityAvailable) as quantityAvailable,
                sum(totalValueBuy)/ sum(quantity) as priceBuy,
                sum(totalValueSell)/ sum(quantity) as priceSell,
                sum(totalValueBuy) as totalValueBuy,
                sum(totalValueSell) as totalValueSell,
                sum(pnl) as pnl
                
                from {cls.query_builder.schema}.expected_pnl
                where idClient = ?
                group by idClient, ticker
                
                order by idClient, ticker
            """
            cur = session.connection().exec_driver_sql(portfolio_sql, tuple([id_client])).cursor
            portfolio = cls.data_frame_factory(cur=cur)
            return expected_pnl, realised_pnl, deposit, portfolio
