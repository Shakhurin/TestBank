import pytest

from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.account.deposit_account_request import DepositAccountRequest
from src.main.api.models.account.transfer_account_request import TransferAccountRequest


@pytest.mark.api
class TestTransferAccount:
    @pytest.mark.parametrize(
        "amount, transfer_amount",
        [
            (9000, 500),
            (9000, 5000),
            (9000, 10000)
        ]
    )
    def test_transfer_account_valid(self, amount, transfer_amount, create_user_request, api_manager, db_session):
        create_first_account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_first_account_request = DepositAccountRequest(accountId=create_first_account_response.id, amount=amount)
        deposit_first_account_response = api_manager.user_steps.deposit_account(deposit_first_account_request,
                                                                                create_user_request)
        deposit_first_account_response = api_manager.user_steps.deposit_account(deposit_first_account_request,
                                                                                create_user_request)

        create_second_account_response = api_manager.user_steps.create_account(create_user_request)

        transfer_account_request = TransferAccountRequest(
            fromAccountId=create_first_account_response.id,
            toAccountId=create_second_account_response.id,
            amount=transfer_amount
        )
        transfer_account_response = api_manager.user_steps.transfer_account(transfer_account_request,
                                                                            create_user_request)

        assert transfer_account_response.fromAccountId == create_first_account_response.id
        assert transfer_account_response.toAccountId == create_second_account_response.id
        assert transfer_account_response.fromAccountIdBalance == deposit_first_account_response.balance - transfer_amount

        db_account_second = AccountCrudDb.get_account_by_id(db_session, create_second_account_response.id)
        db_account_first = AccountCrudDb.get_account_by_id(db_session, create_first_account_response.id)

        assert db_account_second.balance == create_second_account_response.balance + transfer_amount
        assert db_account_first.balance == deposit_first_account_response.balance - transfer_amount

    @pytest.mark.parametrize(
        "amount, transfer_amount",
        [
            (9000, 499.9),
            (9000, 0),
            (9000, 10000.1),
            (9000, -1)
        ]
    )
    def test_transfer_account_invalid(self, amount, transfer_amount, api_manager, create_user_request):
        create_first_account_response = api_manager.user_steps.create_account(create_user_request)
        create_second_account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_first_account_request = DepositAccountRequest(accountId=create_first_account_response.id, amount=amount)
        api_manager.user_steps.deposit_account(deposit_first_account_request, create_user_request)
        api_manager.user_steps.deposit_account(deposit_first_account_request, create_user_request)

        transfer_account_request = TransferAccountRequest(
            fromAccountId=create_first_account_response.id,
            toAccountId=create_second_account_response.id,
            amount=transfer_amount
        )
        transfer_account_response = api_manager.user_steps.transfer_account_invalid(transfer_account_request,
                                                                                    create_user_request)

        if transfer_amount > 0:
            assert "Amount must be between 500 and 10000" in transfer_account_response.json()["error"]
        else:
            assert "Amount must be greater than 0\nAmount must be between 500 and 10000" in \
                   transfer_account_response.json()["error"]
