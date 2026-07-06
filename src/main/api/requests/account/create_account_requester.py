from src.main.api.models.account.create_account_response import CreateAccountResponse
from src.main.api.requests.requester import Requester
import requests

from src.main.api.specs.response_specs import ResponseSpecs


class CreateAccountRequester(Requester):
    def post(self, model=None) -> CreateAccountResponse:
        url=f"{self.base_url}/account/create"
        response = requests.post(
            url=url,
            headers=self.headers
        )
        self.response_spec = ResponseSpecs.request_created()
        return CreateAccountResponse(**response.json())