import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        name='João Silva',
        email='joao@email.com',
        password='senha1234'
    )

@pytest.fixture
def admin(db):
    return User.objects.create_user(
        name='Admin',
        email='admin@email.com',
        password='senha1234',
        is_staff=True
    )

@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def admin_client(client, admin):
    client.force_authenticate(user=admin)
    return client
