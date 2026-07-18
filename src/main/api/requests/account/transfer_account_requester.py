from http import HTTPStatus

from src.main.api.models.account.transfer_account_response import TransferAccountResponse
from src.main.api.requests.requester import Requester
import requests


class TransferAccountRequester(Requester):
    def post(self, transfer_account_request):
        url= f"{self.base_url}/account/transfer"
        response=requests.post(
            url=url,
            json=transfer_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return TransferAccountResponse(**response.json())
        return response