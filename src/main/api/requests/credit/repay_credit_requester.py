from http import HTTPStatus

from src.main.api.requests.requester import Requester
from src.main.api.models.credit.repay_credit_response import RepayCreditResponse


import requests


class RepayCreditRequester(Requester):
    def post(self, repay_credit_request):
        url=f"{self.base_url}/credit/repay"
        response=requests.post(
            url= url,
            json= repay_credit_request.model_dump(),
            headers= self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return RepayCreditResponse(**response.json())
        return response