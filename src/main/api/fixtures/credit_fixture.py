import dataclasses

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.acount_fixture import PreparedCreditAccount
from src.main.api.models.account.create_account_response import CreateAccountResponse
from src.main.api.models.credit.request_credit_request import RequestCreditRequest
from src.main.api.models.credit.request_credit_response import RequestCreditResponse
from src.main.api.models.user.create_user_request import CreateUserRequest
from src.main.api.models.account.create_account_response import CreateAccountResponse


@dataclasses.dataclass(frozen=True)
class PrepareRequestCredit:
    credit_response: RequestCreditResponse
    account: CreateAccountResponse
    user: CreateUserRequest


@pytest.fixture
def prepare_request_credit_account(prepare_credit_account: PreparedCreditAccount, api_manager: ApiManager, request) -> PrepareRequestCredit:
    credit_amount = request.param
    request_credit_request = RequestCreditRequest(accountId=prepare_credit_account.account.id, amount=credit_amount, termMonths=12)
    request_credit_response = api_manager.user_steps.request_credit(request_credit_request, prepare_credit_account.user)
    return PrepareRequestCredit(
        credit_response= request_credit_response,
        user=prepare_credit_account.user,
        account= prepare_credit_account.account
    )