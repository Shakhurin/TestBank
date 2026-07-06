import pytest

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
    def test_request_credit_valid(self, credit_amount, month, create_user_credit_role_request, api_manager, db_session):

        create_account_response = api_manager.user_steps.create_account(create_user_credit_role_request)

        request_credit_request = RequestCreditRequest(accountId=create_account_response.id, amount=credit_amount,
                                                      termMonths=month)

        request_credit_response = api_manager.user_steps.request_credit(request_credit_request,
                                                                        create_user_credit_role_request)
        assert request_credit_response.id == create_account_response.id

        credit_from_db = Credit.get_credit_by_id(db_session, request_credit_response.creditId)
        assert credit_from_db is not None
        assert credit_from_db.id == request_credit_response.creditId
        assert credit_from_db.account_id == create_account_response.id
        assert credit_from_db.amount == credit_amount
        assert credit_from_db.term_months == month

    @pytest.mark.parametrize(
        "credit_amount, month",
        [
            (4999.9, 12),
            (15000.1, 12),
            (0, 12),
            (-100, 12)
        ]
    )
    def test_request_credit_invalid(self, create_user_credit_role_request, credit_amount, month, api_manager,
                                    db_session):

        create_account_response = api_manager.user_steps.create_account(create_user_credit_role_request)

        request_credit_request = RequestCreditRequest(accountId=create_account_response.id, amount=credit_amount,
                                                      termMonths=month)

        request_credit_response = api_manager.user_steps.request_credit_invalid(request_credit_request,
                                                                                create_user_credit_role_request)

        if credit_amount > 0:
            assert "Amount must be between 5000 and 15000" in request_credit_response.json()["error"]
        else:
            assert "Amount must be greater than 0\nAmount must be between 5000 and 15000" in \
                   request_credit_response.json()["error"]

        credit_from_db = Credit.get_credit_by_account_id(db_session, create_account_response.id)
        assert credit_from_db is None, "Кредит создан, ошибка"
