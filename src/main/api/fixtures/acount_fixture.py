import dataclasses

import pytest

from src.main.api.models.account.create_account_response import CreateAccountResponse
from src.main.api.models.account.deposit_account_request import DepositAccountRequest
from src.main.api.models.user.create_user_request import CreateUserRequest

@dataclasses.dataclass(frozen=True)
class PreparedTransferAccounts:
    user: CreateUserRequest
    from_account: CreateAccountResponse
    to_account: CreateAccountResponse
    from_account_balance: float

@dataclasses.dataclass(frozen=True)
class PreparedCreditAccount:
    account: CreateAccountResponse
    user: CreateUserRequest


@pytest.fixture
def account_factory(api_manager):
    def create_account(user):
        return api_manager.user_steps.create_account(user)
    return create_account

@pytest.fixture
def prepare_empty_account(account_factory, create_user_request) -> CreateAccountResponse:
    return account_factory(create_user_request)

@pytest.fixture
def prepare_credit_account(account_factory, create_user_credit_role_request) -> PreparedCreditAccount:
    create_account_response = account_factory(create_user_credit_role_request)
    return PreparedCreditAccount(
        user= create_user_credit_role_request,
        account= create_account_response
    )

@pytest.fixture
def prepared_transfer_accounts(api_manager, account_factory, create_user_request):
    from_account = account_factory(create_user_request)
    to_account = account_factory(create_user_request)

    deposit_from_account_request = DepositAccountRequest(
        accountId=from_account.id,
        amount=9000
    )

    deposit_account_response = api_manager.user_steps.deposit_account(deposit_from_account_request,
                                                                              create_user_request)
    deposit_account_response = api_manager.user_steps.deposit_account(deposit_from_account_request,
                                                                      create_user_request)
    return PreparedTransferAccounts(
        user=create_user_request,
        from_account=from_account,
        to_account=to_account,
        from_account_balance=deposit_account_response.balance
    )