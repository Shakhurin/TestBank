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
    def test_deposit_account_valid(self, amount, prepare_empty_account, create_user_request, api_manager, db_session):
        deposit_account_request = DepositAccountRequest(
            accountId=prepare_empty_account.id,
            amount=amount
        )
        deposit_account_response = api_manager.user_steps.deposit_account(deposit_account_request, create_user_request)

        assert deposit_account_response.id == prepare_empty_account.id, 'ID счета пополнения не соответствует ID созданного счета'
        assert deposit_account_response.balance == amount + prepare_empty_account.balance, 'Баланс увеличился не на переведенную сумму'

        db_account = AccountCrudDb.get_account_by_id(db_session, prepare_empty_account.id)
        assert db_account.balance == amount, 'Увеличился не на переведенную сумму'

    @pytest.mark.parametrize(
        "amount",
        [
            999.99,
            9000.01
        ]
    )
    def test_deposit_account_invalid_positive_nums(self, amount, empty_account, create_user_request, api_manager,
                                                   db_session):
        deposit_account_request = DepositAccountRequest(
            accountId=empty_account.id,
            amount=amount
        )

        deposit_account_response = api_manager.user_steps.deposit_account_invalid(deposit_account_request,
                                                                                  create_user_request)

        assert deposit_account_response.json()[
                   "error"] == "Amount must be between 1000 and 9000", 'Сумма в диапазоне 1000-9000'

        db_account = AccountCrudDb.get_account_by_id(db_session, empty_account.id)
        assert db_account.balance == 0, 'Баланс не равен нулю'
