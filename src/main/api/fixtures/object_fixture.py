import logging
from typing import Any, List

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.user.create_user_response import CreateUserResponse


@pytest.fixture
def created_obj():
    objects: List[Any] = []
    yield objects
    clean_user(objects)


def clean_user(objects: List[Any]):
    api_manager = ApiManager(objects)
    for i in objects:
        if isinstance(i, CreateUserResponse):
            api_manager.admin_steps.delete_user(i.id)
        else:
            logging.warning(f"Error in delete user_id: {i.id}")