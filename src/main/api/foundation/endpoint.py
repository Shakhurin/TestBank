from enum import Enum

from src.main.api.models.account.create_account_response import CreateAccountResponse
from src.main.api.models.account.deposit_account_request import DepositAccountRequest
from src.main.api.models.account.deposit_account_response import DepositAccountResponse
from src.main.api.models.account.transfer_account_request import TransferAccountRequest
from src.main.api.models.account.transfer_account_response import TransferAccountResponse
from src.main.api.models.auth.login_user_response import LoginUserResponse
from src.main.api.models.base_model import BaseModel
from typing import Optional, Type
from dataclasses import dataclass

from src.main.api.models.credit.repay_credit_request import RepayCreditRequest
from src.main.api.models.credit.repay_credit_response import RepayCreditResponse
from src.main.api.models.credit.request_credit_request import RequestCreditRequest
from src.main.api.models.credit.request_credit_response import RequestCreditResponse
from src.main.api.models.user.create_user_request import CreateUserRequest
from src.main.api.models.user.create_user_response import CreateUserResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model=None,
        url="/auth/token/login",
        response_model=LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=CreateAccountResponse
    )

    DEPOSIT_ACCOUNT = EndpointConfiguration(
        request_model= DepositAccountRequest,
        url="/account/deposit",
        response_model=DepositAccountResponse
    )

    TRANSFER_ACCOUNT = EndpointConfiguration(
        request_model= TransferAccountRequest,
        url="/account/transfer",
        response_model= TransferAccountResponse
    )

    CREDIT_REQUEST = EndpointConfiguration(
        request_model=RequestCreditRequest,
        url="/credit/request",
        response_model=RequestCreditResponse
    )

    CREDIT_REPAY = EndpointConfiguration(
        request_model=RepayCreditRequest,
        url="/credit/repay",
        response_model=RepayCreditResponse
    )