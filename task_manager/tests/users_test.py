import pytest
from ..users.models import CustomUser
from .conftest import authenticated_client, form_data, user
from django.test import Client
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.db import transaction
from ..forms import LoginForm
import pytest
from django.contrib.auth import authenticate


@pytest.mark.urls('task_manager.urls')
def test_user_create_valid_data(form_data, db):
    client = Client()
    with transaction.atomic():
        CustomUser.objects.filter(username=form_data['username']).delete()
    url = reverse('users:users_create')
    response = client.post(url, data=form_data)
    assert response.status_code == 302
    created_user = CustomUser.objects.get(username=form_data['username'])
    assert created_user.username == form_data['username']
    assert check_password(form_data['password'], created_user.password)
    assert created_user.name == form_data['name']
    assert created_user.surname == form_data['surname']


@pytest.mark.urls('task_manager.urls')
def test_user_create_invalid_data(invalid_form_data, db):
    client = Client()
    url = reverse('users:users_create')
    response = client.post(url, data=invalid_form_data)
    assert response.status_code != 302
    username_to_check = invalid_form_data['username']
    users_count = CustomUser.objects.filter(username=username_to_check).count()
    assert users_count == 0


@pytest.mark.django_db
def test_login_valid_data(form_data):
    client = Client()
    with transaction.atomic():
        CustomUser.objects.filter(username=form_data['username']).delete()
    # Предполагается, что form_data содержит корректные данные для входа
    username = form_data['username']
    password = form_data['password']

    # Отправляем POST-запрос к URL-адресу входа в систему
    url = reverse('login')  # Замените 'users:login' на актуальный путь к вашему view функции входа
    response = client.post(url, {'username': username, 'password': password})

    # Проверяем статус ответа
    assert response.status_code == 302  # Обычно успешный вход приводит к редиректу

    # Проверяем, аутентифицирован ли пользователь
    user = authenticate(username=username, password=password)
    assert user is not None

    # Проверяем, что пользователь вошел в систему
    assert client.session['_auth_user_id'] == str(user.id)


@pytest.mark.django_db
def test_login_valid_data(form_data):
    client = Client()
    username = form_data['username']
    password = form_data['password']
    user = CustomUser.objects.create_user(username=username, password=password)
    url = reverse('login')
    response = client.post(url, {'username': username, 'password': password})
    assert response.status_code == 302, "Expected redirect after successful login"


@pytest.mark.django_db
def test_login_valid_data(form_data):
    client = Client()
    username = form_data['username']
    password = form_data['password']
    user = CustomUser.objects.create_user(username=username, password=password)
    url = reverse('login')
    response = client.post(url, {'username': username, 'password': 'wrong'})
    assert response.status_code != 302, "Expected redirect after successful login"
