import pytest

from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.fixtures.user_fixture import create_user_request
from src.main.api.models.account.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb


@pytest.mark.api
class TestDepositAccount:
    @pytest.mark.parametrize(
        "amount",
        [
            1000,
            4500,
            9000
        ]
    )
    def test_deposit_account_valid(self, amount, create_user_request, api_manager, db_session):
        create_account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_account_request = DepositAccountRequest(
            accountId=create_account_response.id,
            amount=amount
        )
        deposit_account_response = api_manager.user_steps.deposit_account(deposit_account_request, create_user_request)

        assert deposit_account_response.id == create_account_response.id
        assert deposit_account_response.balance == amount + create_account_response.balance

        db_account = AccountCrudDb.get_account_by_id(db_session,create_account_response.id)
        assert db_account is not None
        assert db_account.balance == amount

    @pytest.mark.parametrize(
        "amount",
        [
            999.99,
            0,
            -100,
            9000.01
        ]
    )
    def test_deposit_account_invalid(self, amount, api_manager, create_user_request, db_session):
        create_account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_account_request = DepositAccountRequest(
            accountId=create_account_response.id,
            amount=amount
        )

        deposit_account_response = api_manager.user_steps.deposit_account_invalid(deposit_account_request,
                                                                                  create_user_request)

        if amount > 0:
            assert deposit_account_response.json()["error"] == "Amount must be between 1000 and 9000"
        else:
            assert deposit_account_response.json()[
                       "error"] == "Amount must be greater than 0\nAmount must be between 1000 and 9000"

        db_account = AccountCrudDb.get_account_by_id(db_session,create_account_response.id)
        assert db_account.balance == 0