import numpy as np
import pandas as pd
from src.common.consts import MessageConsts
from src.common.responses.exceptions import BaseExceptionResponse
from src.modules.auth.dtos import TokenPayloadDTO
from src.modules.brokers.repositories import BrokerRepo
from src.modules.clients.repositories import ClientRepo, UserClientMembershipRepo


class ClientService:
    def __init__(self):
        self.client_repo = ClientRepo
        self.broker_repo = BrokerRepo
        self.user_client_membership_repo = UserClientMembershipRepo

    # def add_client(self, current_user: TokenPayloadDTO, payload: AddClientPayloadDTO):
    #     brokers = self.broker_repo.get_by_id(_id=payload.brokerID)
    #     if len(brokers) == 0:
    #         raise BaseExceptionResponse(
    #             http_code=400,
    #             status_code=400,
    #             message=MessageConsts.BAD_REQUEST,
    #             errors={"brokerID": ["brokerID is not exists"]}
    #         )
    #     with self.client_repo.session_scope():
    #         data = payload.dict()
    #         client = self.client_repo.insert(record=data, returning=True)
    #         ucm = {
    #             UserClientMembership.userID.name: current_user[User.id.name],
    #             UserClientMembership.clientID.name: client[Client.id.name],
    #             UserClientMembership.role.name: UCMRoleEnum.ADMIN.value,
    #         }
    #         self.user_client_membership_repo.insert(record=ucm, returning=False)
    #         self.user_client_membership_repo.add_admin_membership(client=client, user=current_user)
    #     return client

    def get_client_pagination(self, current_user: TokenPayloadDTO, page: int, pageSize: int, brokerName, id_client: str = None):
        return self.user_client_membership_repo.pagination_client_by_current_user(
            current_user=current_user, page=page, pageSize=pageSize, id_client=id_client, brokerName=brokerName
        )

    def get_report_by_id_client(self, id_client: str):
        expected_pnl_raw, realised_pnl_raw, deposit_raw, portfolio_raw = self.client_repo.get_report_by_id_client(
            id_client=id_client)
        expected_pnl_cols = [
            "totalValueBuy", "totalValueSell", "totalValueLoan", "costBuy", "costSell",
            "costLoanFromDayLoan", "costLoanFromDayAdvance", "costLoan", "pnl", "minDeposit"
        ]
        realised_pnl_cols = [
            "totalValueBuy", "totalValueSell", "totalValueLoan", "costBuy", "costSell",
            "costLoanFromDayLoan", "costLoanFromDayAdvance", "costLoan", "pnl"
        ]
        deposit_cols = ["deposit"]

        expectedPNL = pd.DataFrame(expected_pnl_raw[expected_pnl_cols].sum(axis=0)).T
        realisedPNL = pd.DataFrame(realised_pnl_raw[realised_pnl_cols].sum(axis=0)).T
        deposit = pd.DataFrame(deposit_raw[deposit_cols].sum(axis=0)).T
        assets = pd.DataFrame([[]])
        assets["totalValueLoan"] = expectedPNL["totalValueLoan"].iloc[0]
        assets["deposit"] = deposit["deposit"].iloc[0]
        assets["realisedPNL"] = realisedPNL["pnl"].iloc[0]
        assets["expectedPNL"] = expectedPNL["pnl"].iloc[0]
        assets["minDeposit"] = expectedPNL["minDeposit"].iloc[0]
        assets["nav"] = assets["deposit"] + assets["realisedPNL"] + assets["expectedPNL"]
        total_value_sell = expectedPNL["totalValueLoan"].iloc[0]
        assets["coverageRatio"] = None if total_value_sell == 0 else assets["nav"]/total_value_sell
        assets["remain"] = assets["nav"] - assets["minDeposit"]
        assets["pnl"] = assets["realisedPNL"] - assets["expectedPNL"]
        assets["purchasingPower"] = assets["remain"]*5
        expected_pnl_raw = pd.concat([expected_pnl_raw, expectedPNL], ignore_index=True).replace({np.nan: None})
        realised_pnl_raw = pd.concat([realised_pnl_raw, realisedPNL], ignore_index=True).replace({np.nan: None})
        deposit_raw = pd.concat([deposit_raw, deposit], ignore_index=True).replace({np.nan: None})
        results = {
            "expectedPNL": {"schema": list(expected_pnl_raw.columns), "records": expected_pnl_raw.round(3).values.tolist()},
            "realisedPNL": {"schema": list(realised_pnl_raw.columns), "records": realised_pnl_raw.round(3).values.tolist()},
            "deposite": {"schema": list(deposit_raw.columns), "records": deposit_raw.round(3).values.tolist()},
            "portfolio": {"schema": list(portfolio_raw.columns), "records": portfolio_raw.round(3).values.tolist()},
            "assets": {"schema": list(assets.columns), "records": assets.round(3).values.tolist()}
        }
        return results

    def get_management_by_broker_name(self, broker_name: str, page: int, pageSize: int):
        management, total = self.client_repo.get_management_by_broker_name(broker_name=broker_name, page=page, pageSize=pageSize)
        management = management.replace({np.nan: None})
        return {"schema": list(management.columns), "records": management.round(3).values.tolist()}, total

    def get_portfolio_by_broker_name(self, broker_name: str):
        portfolio = self.client_repo.get_portfolio_by_broker_name(broker_name=broker_name)
        portfolio = portfolio.replace({np.nan: None})
        return {"schema": list(portfolio.columns), "records": portfolio.round(3).values.tolist()}
