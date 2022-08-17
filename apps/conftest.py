from django.test import Client

from rest_framework.test import APIClient

import pytest

from .users.factories import UserFactory
from .users.models import User


@pytest.fixture
def api_client() -> APIClient:
    """Create api client."""
    return APIClient()


@pytest.fixture(scope="session")
def user(django_db_blocker) -> User:
    """Fixture for user."""
    with django_db_blocker.unblock():
        return UserFactory()


@pytest.fixture
def auth_client(client: Client, user: User):
    """Authenticated client."""
    client.force_login(user)
    return client
