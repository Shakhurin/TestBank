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
        "credit_amount, repay_amount",
        [
            (5000, 5000),
            (15000, 15000)
        ]
    )
    def test_repay_credit_valid(self, api_manager, credit_amount, repay_amount, create_user_credit_role_request):
        create_account_response = api_manager.user_steps.create_account(create_user_credit_role_request)

        request_credit_request = RequestCreditRequest(accountId=create_account_response.id, amount=credit_amount,
                                                      termMonths=12)

        request_credit_response = api_manager.user_steps.request_credit(request_credit_request, create_user_credit_role_request)

        repay_credit_request = RepayCreditRequest(creditId=request_credit_response.creditId,
                                                  accountId=create_account_response.id, amount=repay_amount)

        repay_credit_response = api_manager.user_steps.repay_credit(repay_credit_request,create_user_credit_role_request)

        assert repay_credit_response.creditId == repay_credit_request.creditId

    @pytest.mark.parametrize(
        "credit_amount, repay_amount",
        [
            (5001, 5000),
            (15000, 20000),
            (7000, 0),
            (7000, -1000),

        ]
    )
    def test_repay_credit_invalid(self, credit_amount, repay_amount, api_manager, create_user_credit_role_request):
        create_account_response = api_manager.user_steps.create_account(create_user_credit_role_request)

        request_credit_request = RequestCreditRequest(accountId=create_account_response.id, amount=credit_amount,
                                                      termMonths=12)

        request_credit_response = api_manager.user_steps.request_credit(request_credit_request,
                                                                        create_user_credit_role_request)

        repay_credit_request = RepayCreditRequest(creditId=request_credit_response.creditId,
                                                  accountId=create_account_response.id, amount=repay_amount)

        repay_credit_response = api_manager.user_steps.repay_credit_invalid(repay_credit_request,
                                                                    create_user_credit_role_request)

        if repay_amount <= 0:
            assert repay_credit_response.status_code == 400
            assert "Amount must be greater than 0" in repay_credit_response.json()["error"]
        elif 0 < repay_amount < credit_amount:
            assert repay_credit_response.status_code == 422
            assert "The amount is not enough" in repay_credit_response.json()["error"]
        elif repay_amount > credit_amount:
            assert repay_credit_response.status_code == 422
            assert "Insufficient funds" in repay_credit_response.json()["error"]