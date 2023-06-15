from typing import Dict, List
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
        results = [list(item) for item in cur.fetchall()]
        results = pd.DataFrame(results, columns=columns)
        return results

    @classmethod
    def get_by_id_client(cls, id_client: str) -> List[Dict]:
        sql = f"""
            select *
            from {cls.query_builder.full_table_name}
            where idClient=?
        """
        with cls.session_scope() as session:
            cur = session.connection().exec_driver_sql(sql, tuple([id_client])).cursor
            records = cls.row_factory(cur=cur)
        return records

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

    @classmethod
    def get_management_by_broker_name(cls, broker_name: str, page, pageSize):
        with cls.session_scope() as session:
            sql = f"""
                select
                s0.idClient,
                s0.nameClient,
                s1.deposit,
                s1.nav,
                s2.totalValueSell,
                s1.nav / s2.totalValueSell as depositRate,
                s2.minDeposit,
                s1.nav - s2.minDeposit as remainingDeposit,
                s1.nav - s2.minDeposit as withdraw,
                s1.pnl,
                (s1.nav - s2.minDeposit) * 5 as purchasingPower,
                s2.costBuyExpected,
                s2.costSellExpected,
                s2.costLoanFromDayLoanExpected,
                s2.costLoanFromDayAdvanceExpected,
                s2.costLoanExpected,
                s3.costBuyRealised,
                s3.costSellRealised,
                s3.costLoanFromDayLoanRealised,
                s3.costLoanFromDayAdvanceRealised,
                s3.costLoanRealised

                from

                (select nameBroker, idClient, nameClient from trading.client) s0

                left join

                --nav
                (select idClient,
                sum(deposit) as deposit,
                sum(pnl) as pnl,
                sum(nav) as nav
                from
                (
                select idClient, deposit, 0 as pnl, deposit as nav from trading.deposit
                union all
                select idClient, 0 as deposit, pnl, pnl as nav from trading.realised_pnl
                union all
                select idClient, 0 as deposit, pnl, pnl as nav from trading.expected_pnl) as s
                group by idClient) s1
                on s0.idClient = s1.idClient

                left join

                -- portfolio
                (select idClient,
                max(__createdAt__) as __createdAt__,
                max(__updatedAt__) as __updatedAt__,
                sum(totalValueSell) as totalValueSell,
                sum(minDeposit) as minDeposit,
                sum(costBuy) as costBuyExpected,
                sum(costSell) as costSellExpected,
                sum(costLoanFromDayLoan) as costLoanFromDayLoanExpected,
                sum(costLoanFromDayAdvance) as costLoanFromDayAdvanceExpected,
                sum(costLoan) as costLoanExpected
                from trading.expected_pnl
                group by idClient) s2

                on s0.idClient = s2.idClient

                left join

                -- cost realised
                (select idClient,
                sum(costBuy) as costBuyRealised,
                sum(costSell) as costSellRealised,
                sum(costLoanFromDayLoan) as costLoanFromDayLoanRealised,
                sum(costLoanFromDayAdvance) as costLoanFromDayAdvanceRealised,
                sum(costLoan) as costLoanRealised
                from trading.realised_pnl
                group by idClient) s3

                on s0.idClient = s3.idClient
                where s0.nameBroker = ?
                order by s0.idClient
                OFFSET ? ROWS
                FETCH NEXT ? ROWS ONLY;
            """
            count_sql = """
                select count(*) as total

                from

                (select nameBroker, idClient, nameClient from trading.client) s0

                left join

                --nav
                (select idClient,
                sum(deposit) as deposit,
                sum(pnl) as pnl,
                sum(nav) as nav
                from
                (
                select idClient, deposit, 0 as pnl, deposit as nav from trading.deposit
                union all
                select idClient, 0 as deposit, pnl, pnl as nav from trading.realised_pnl
                union all
                select idClient, 0 as deposit, pnl, pnl as nav from trading.expected_pnl) as s
                group by idClient) s1
                on s0.idClient = s1.idClient

                left join

                -- portfolio
                (select idClient,
                max(__createdAt__) as __createdAt__,
                max(__updatedAt__) as __updatedAt__,
                sum(totalValueSell) as totalValueSell,
                sum(minDeposit) as minDeposit,
                sum(costBuy) as costBuyExpected,
                sum(costSell) as costSellExpected,
                sum(costLoanFromDayLoan) as costLoanFromDayLoanExpected,
                sum(costLoanFromDayAdvance) as costLoanFromDayAdvanceExpected,
                sum(costLoan) as costLoanExpected
                from trading.expected_pnl
                group by idClient) s2

                on s0.idClient = s2.idClient

                left join

                -- cost realised
                (select idClient,
                sum(costBuy) as costBuyRealised,
                sum(costSell) as costSellRealised,
                sum(costLoanFromDayLoan) as costLoanFromDayLoanRealised,
                sum(costLoanFromDayAdvance) as costLoanFromDayAdvanceRealised,
                sum(costLoan) as costLoanRealised
                from trading.realised_pnl
                group by idClient) s3

                on s0.idClient = s3.idClient
                where s0.nameBroker = ?
            """
            cur = session.connection().exec_driver_sql(count_sql, tuple([broker_name])).cursor
            total = cls.row_factory(cur=cur)[0]["total"]
            cur = session.connection().exec_driver_sql(sql, tuple([broker_name, page*pageSize, pageSize])).cursor
            managment = cls.data_frame_factory(cur=cur)
            return managment, total

    @classmethod
    def get_portfolio_by_broker_name(cls, broker_name: str):
        with cls.session_scope() as session:
            sql = f"""
                select ticker, quantity, quantityAvailable, priceBuy, priceSell, totalValueBuy, totalValueSell, pnl
                from
                (select 
                nameBroker,idClient, ticker, 
                max(__createdAt__) as __createdAt__, max(__updatedAt__) as __updatedAt__ , 
                sum(quantity) as quantity, 
                sum(quantityAvailable) as quantityAvailable,
                sum(totalValueBuy)/ sum(quantity) as priceBuy,
                sum(totalValueSell)/ sum(quantity) as priceSell,
                sum(totalValueBuy) as totalValueBuy,
                sum(totalValueSell) as totalValueSell,
                sum(pnl) as pnl
                
                from trading.expected_pnl
                group by nameBroker, idClient, ticker
                
                ) as s
                where nameBroker = ?
                order by nameBroker, idClient, ticker 
            """
            cur = session.connection().exec_driver_sql(sql, tuple([broker_name])).cursor
            portfolio = cls.data_frame_factory(cur=cur)
            return portfolio
