from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.account.deposit_account_request import DepositAccountRequest
from src.main.api.models.account.transfer_account_request import TransferAccountRequest
from src.main.api.models.credit.repay_credit_request import RepayCreditRequest
from src.main.api.models.credit.request_credit_request import RequestCreditRequest
from src.main.api.models.user.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit_account(self, deposit_account_request: DepositAccountRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        return response

    def deposit_account_invalid(self, deposit_account_request: DepositAccountRequest,
                                create_user_request: CreateUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(deposit_account_request)
        return response

    def transfer_account(self, transfer_account_request: TransferAccountRequest,
                         create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(transfer_account_request)
        return response

    def transfer_account_invalid(self, transfer_account_request: TransferAccountRequest,
                                 create_user_request: CreateUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(transfer_account_request)
        return response

    def request_credit(self, request_credit_request: RequestCreditRequest, create_user_credit_role_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_credit_role_request.username,
                password=create_user_credit_role_request.password
            ),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(request_credit_request)
        return response

    def request_credit_invalid(self, request_credit_request: RequestCreditRequest, create_user_credit_role_request: CreateUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_credit_role_request.username,
                password=create_user_credit_role_request.password
            ),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad()
        ).post(request_credit_request)
        return response

    def repay_credit(self, repay_credit_request: RepayCreditRequest, create_user_credit_role_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_credit_role_request.username,
                password=create_user_credit_role_request.password
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(repay_credit_request)
        return response

    def repay_credit_invalid(self, repay_credit_request: RepayCreditRequest, create_user_credit_role_request: CreateUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_credit_role_request.username,
                password=create_user_credit_role_request.password
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unauthorized()
        ).post(repay_credit_request)
        return response