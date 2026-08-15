import pytest
from requests import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.acount_fixture import PreparedCreditAccount
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.credit.request_credit_request import RequestCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrud as Credit


class TestRequestCredit:
    @pytest.mark.parametrize(
        "credit_amount, month",
        [
            (5000, 12),
            (15000, 12)
        ]
    )
    def test_request_credit_valid(self, credit_amount:float, month: int, prepare_credit_account: PreparedCreditAccount,
                                  api_manager: ApiManager, db_session: Session):
        request_credit_request = RequestCreditRequest(accountId=prepare_credit_account.account.id, amount=credit_amount,
                                                      termMonths=month)

        request_credit_response = api_manager.user_steps.request_credit(request_credit_request,
                                                                        prepare_credit_account.user)
        assert request_credit_response.id == prepare_credit_account.account.id, 'Кредит запрошен на другой счет'

        credit_from_db = Credit.get_credit_by_id(db_session, request_credit_response.creditId)
        assert credit_from_db.id == request_credit_response.creditId, 'Кредит запрошен на другой счет'
        assert credit_from_db.amount == credit_amount, f'Кредит взят не на сумму: {credit_amount}'
        assert credit_from_db.term_months == month, f'Кредит запрошен не на {month} месяцев'

    @pytest.mark.parametrize(
        "credit_amount, month",
        [
            (4999.9, 12),
            (15000.1, 12),
        ]
    )
    def test_request_credit_invalid(self, prepare_credit_account: PreparedCreditAccount, credit_amount: float, month: int,
                                    api_manager: ApiManager, db_session: Session):
        request_credit_request = RequestCreditRequest(accountId=prepare_credit_account.account.id, amount=credit_amount,
                                                      termMonths=month)

        request_credit_response = api_manager.user_steps.request_credit_invalid(request_credit_request,
                                                                                prepare_credit_account.user)

        assert "Amount must be between 5000 and 15000" in request_credit_response.json()[
            "error"], 'Кредит запрошен на сумму в диапазоне 5000-15000'

        credit_from_db = Credit.get_credit_by_account_id(db_session, prepare_credit_account.account.id)
        assert credit_from_db is None, "Кредит создан, ошибка"
