from http import HTTPStatus
from requests import Response


class ResponseSpecs:
    @staticmethod
    def request_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod
    def request_created():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    @staticmethod
    def request_bad():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    @staticmethod
    def bad_or_request_unprocess():
        def confirm(response: Response):
            assert response.status_code in [HTTPStatus.UNPROCESSABLE_ENTITY, HTTPStatus.BAD_REQUEST], response.text
        return confirm