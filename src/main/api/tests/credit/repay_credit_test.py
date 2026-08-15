import pytest, requests, uuid

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.credit.repay_credit_request import RepayCreditRequest
from src.main.api.fixtures.credit_fixture import PrepareRequestCredit
from src.main.api.models.user.create_user_request import CreateUserCreditRoleRequest


@pytest.mark.api
class TestRepayCredit:
    @pytest.mark.parametrize(
        "prepare_request_credit_account, repay_amount",
        [
            (5000, 5000),
            (15000, 15000)
        ],
        indirect=["prepare_request_credit_account"]
    )
    def test_repay_credit_valid(self, api_manager: ApiManager, repay_amount: float,
                                prepare_request_credit_account: PrepareRequestCredit,
                                create_user_credit_role_request: CreateUserCreditRoleRequest):
        repay_credit_request = RepayCreditRequest(creditId=prepare_request_credit_account.credit_response.creditId,
                                                  accountId=prepare_request_credit_account.account.id,
                                                  amount=repay_amount)

        repay_credit_response = api_manager.user_steps.repay_credit(repay_credit_request,
                                                                    create_user_credit_role_request)

        assert repay_credit_response.creditId == repay_credit_request.creditId

    @pytest.mark.parametrize(
        "prepare_request_credit_account, repay_amount",
        [
            (7000, 0),
            (7000, -1000),
        ],
        indirect=["prepare_request_credit_account"]
    )
    def test_repay_credit_invalid(self, repay_amount: float, api_manager: ApiManager,
                                  prepare_request_credit_account: PrepareRequestCredit,
                                  create_user_credit_role_request: CreateUserCreditRoleRequest):
        repay_credit_request = RepayCreditRequest(creditId=prepare_request_credit_account.credit_response.creditId,
                                                  accountId=prepare_request_credit_account.account.id,
                                                  amount=repay_amount)

        repay_credit_response = api_manager.user_steps.repay_credit_invalid(repay_credit_request,
                                                                            create_user_credit_role_request)

        assert repay_credit_response.status_code == 400, 'Запрос прошел успешно'
        assert "Amount must be greater than 0" in repay_credit_response.json()["error"], 'Погашение было больше нуля'
