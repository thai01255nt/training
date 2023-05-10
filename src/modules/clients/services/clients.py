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

    def get_client_pagination(self, current_user: TokenPayloadDTO, page: int, pageSize: int, id_client: str = None):
        return self.user_client_membership_repo.pagination_client_by_current_user(
            current_user=current_user, page=page, pageSize=pageSize, id_client=id_client
        )

    def get_report_by_id_client(self, id_client: str):
        expected_pnl, realised_pnl, deposit, portfolio = self.client_repo.get_report_by_id_client(id_client=id_client)
        summary = {}
        summary["expectedPNL"] = {} if len(expected_pnl) == 0 else pd.DataFrame(expected_pnl)[[
            "totalValueBuy", "totalValueSell", "totalValueLoan", "costBuy", "costSell",
            "costLoanFromDayLoan", "costLoanFromDayAdvance", "costLoan", "pnl", "minDeposit"
        ]].sum(axis=0).to_dict() 
        summary["realisedPNL"] = {} if len(realised_pnl) == 0 else pd.DataFrame(realised_pnl)[[
            "totalValueBuy", "totalValueSell", "totalValueLoan", "costBuy", "costSell",
            "costLoanFromDayLoan", "costLoanFromDayAdvance", "costLoan", "pnl"
        ]].sum(axis=0).to_dict()
        summary["deposit"] = {} if len(deposit) == 0 else pd.DataFrame(deposit)[["deposit"]].sum(axis=0).to_dict()

        summary["assets"] = {
            "totalValueLoan": summary["expectedPNL"].get("totalValueLoan", 0),
            "deposit": summary["deposit"].get("deposit", 0),
            "realisedPNL": summary["realisedPNL"].get("pnl", 0),
            "expectedPNL": summary["expectedPNL"].get("pnl", 0),
            "minDeposit": summary["expectedPNL"].get("minDeposit", 0),
        }
        summary["assets"]["nav"] = summary["assets"]["deposit"] + summary["assets"]["realisedPNL"] + summary["assets"]["expectedPNL"]
        total_value_sell = summary["expectedPNL"].get("totalValueSell", 0)
        summary["assets"]["coverageRatio"] = None if total_value_sell == 0 else summary["assets"]["nav"]/total_value_sell
        summary["assets"]["remain"] = summary["assets"]["nav"] - summary["assets"]["minDeposit"]
        summary["assets"]["pnl"] = summary["assets"]["realisedPNL"] - summary["assets"]["expectedPNL"]
        summary["assets"]["purchasingPower"] = summary["assets"]["remain"]*5
        results = {
            "expectedPNL": expected_pnl,
            "realisedPNL": realised_pnl,
            "deposite": deposit,
            "portfolio": portfolio,
            "summary": summary
        }
        return results
