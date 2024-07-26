import pytest
from django.test import Client
from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):  # Использование фикстуры db для доступа к базе данных
    """Фикстура для создания экземпляра CustomUserModel."""
    CustomUserModel = get_user_model()
    user = CustomUserModel.objects.create_user(username='testuser', password='testpass')
    return user


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture(params=[{'name': 'testname', 'surname': 'testsurname', 'username': 'testuser',
                         'password': 'testpassword', 'password2': 'testpassword'}])
def form_data(request):
    return request.param
