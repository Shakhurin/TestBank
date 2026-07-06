from http import HTTPStatus

from src.main.api.requests.requester import Requester
from src.main.api.models.user.create_user_request import CreateUserRequest
import requests


class CreateUserRequester(Requester):
    def post(self, create_user_request:CreateUserRequest):
        url = f"{self.base_url}/admin/create"
        response = requests.post(
            url = url,
            json=create_user_request.model_dump(),
            headers = self.headers
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return CreateUserRequest(**response.json())
        return response