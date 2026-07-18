import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.user.create_user_request import CreateUserRequest, CreateUserCreditRoleRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_user_credit_role_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserCreditRoleRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request