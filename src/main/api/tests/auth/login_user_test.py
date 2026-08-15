import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.auth.login_user_request import LoginUserRequest
from src.main.api.models.user.create_user_request import CreateUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager):
        login_user_request = LoginUserRequest(
            username="admin",
            password="123456"
        )

        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username, 'Создали другого пользователя'
        assert response.user.role == "ROLE_ADMIN", 'Роль отличается от Admin'

    def test_login_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, 'Создали другого пользователя'
        assert response.user.role == "ROLE_USER", 'Роль отличается от User'

    @pytest.mark.parametrize(
        'username, password',
        [
            ('Admin', '123456'),
            ('admin', '1234567'),
            ('wrong_login', 'not_a_password')
        ]
    )
    def test_login_admin_invalid(self, api_manager: ApiManager, username: str, password: str):
        login_user_request_invalid = LoginUserRequest(
            username= username,
            password= password
        )

        response = api_manager.admin_steps.login_user_invalid(login_user_request_invalid)
        assert response.status_code == 401, 'Авторизовался админом под невалидными кредами'