import pytest

from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.account.deposit_account_request import DepositAccountRequest
from src.main.api.models.account.transfer_account_request import TransferAccountRequest


@pytest.mark.api
class TestTransferAccount:
    @pytest.mark.parametrize(
        "transfer_amount",
        [
            500,
            5000,
            10000
        ]
    )
    def test_transfer_account_valid(self, prepared_transfer_accounts, transfer_amount, create_user_request, api_manager,
                                    db_session):
        transfer_account_request = TransferAccountRequest(
            fromAccountId=prepared_transfer_accounts.from_account.id,
            toAccountId=prepared_transfer_accounts.to_account.id,
            amount=transfer_amount
        )
        transfer_account_response = api_manager.user_steps.transfer_account(transfer_account_request,
                                                                            create_user_request)

        assert transfer_account_response.fromAccountId == prepared_transfer_accounts.from_account.id, 'Деньги списались не с того счета'
        assert transfer_account_response.toAccountId == prepared_transfer_accounts.to_account.id, 'Деньги ушли не на тот счет'
        assert transfer_account_response.fromAccountIdBalance == prepared_transfer_accounts.from_account_balance - transfer_amount, 'Списалось не то количество денег'

        db_account_second = AccountCrudDb.get_account_by_id(db_session, prepared_transfer_accounts.to_account.id)
        db_account_first = AccountCrudDb.get_account_by_id(db_session, prepared_transfer_accounts.from_account.id)

        assert db_account_second.balance == prepared_transfer_accounts.to_account.balance + transfer_amount, f'Получена не сумма {transfer_amount}'
        assert db_account_first.balance == prepared_transfer_accounts.from_account_balance - transfer_amount, f'Переведена не сумма {transfer_amount}'

    @pytest.mark.parametrize(
        "transfer_amount",
        [
            499.9,
            10000.1,
        ]
    )
    def test_transfer_account_invalid(self, prepared_transfer_accounts, transfer_amount, api_manager,
                                      create_user_request):
        transfer_account_request = TransferAccountRequest(
            fromAccountId=prepared_transfer_accounts.from_account.id,
            toAccountId=prepared_transfer_accounts.to_account.id,
            amount=transfer_amount
        )
        transfer_account_response = api_manager.user_steps.transfer_account_invalid(transfer_account_request,
                                                                                    create_user_request)

        assert "Amount must be between 500 and 10000" in transfer_account_response.json()[
            "error"], 'Переведена сумма в диапазоне 500-10000'
