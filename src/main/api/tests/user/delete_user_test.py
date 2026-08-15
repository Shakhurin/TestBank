import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixture import api_manager


@pytest.mark.api
class TestDeleteUser:
    def test_delete_user(self, api_manager: ApiManager, create_user_for_delete_request: int):
        delete_user_response = api_manager.admin_steps.delete_user(create_user_for_delete_request)

        assert delete_user_response.status_code == 200, 'Пользователь не удален'
