import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.user.create_user_request import CreateUserRequest, CreateUserCreditRoleRequest


@pytest.fixture
def create_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_user_credit_role_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserCreditRoleRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_user_for_delete_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    created_user = api_manager.admin_steps.create_user(user_request)
    yield created_user.id
    