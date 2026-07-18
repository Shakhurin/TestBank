import pytest, requests, uuid

from src.main.api.models.credit.repay_credit_request import RepayCreditRequest
from src.main.api.models.credit.request_credit_request import RequestCreditRequest
from src.main.api.models.user.create_user_request import CreateUserRequest
from src.main.api.requests.credit.request_credit_requester import RequestCreditRequester
from src.main.api.requests.user.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.account.create_account_requester import CreateAccountRequester
from src.main.api.requests.credit.repay_credit_requester import RepayCreditRequester


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
    def test_repay_credit_valid(self, api_manager, repay_amount, prepare_request_credit_account,
                                create_user_credit_role_request):
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
    def test_repay_credit_invalid(self, repay_amount, api_manager, prepare_request_credit_account, create_user_credit_role_request):
        repay_credit_request = RepayCreditRequest(creditId=prepare_request_credit_account.credit_response.creditId,
                                                  accountId=prepare_request_credit_account.account.id, amount=repay_amount)

        repay_credit_response = api_manager.user_steps.repay_credit_invalid(repay_credit_request,
                                                                            create_user_credit_role_request)

        assert repay_credit_response.status_code == 400, 'Запрос прошел успешно'
        assert "Amount must be greater than 0" in repay_credit_response.json()["error"], 'Погашение было больше нуля'
