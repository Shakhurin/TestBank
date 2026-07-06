from http import HTTPStatus

import requests
from src.main.api.models.credit.request_credit_response import RequestCreditResponse
from src.main.api.requests.requester import Requester


class RequestCreditRequester(Requester):
    def post(self, request_credit_request):
        url= f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=request_credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.CREATED:
            return RequestCreditResponse(**response.json())
        return response