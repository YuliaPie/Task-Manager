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
from django.contrib.messages import get_messages


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
    username = form_data['username']
    password = form_data['password']
    user = CustomUser.objects.create_user(username=username, password=password)
    url = reverse('login')
    response = client.post(url, {'username': username, 'password': password})
    assert response.status_code == 302, "Expected redirect after successful login"


@pytest.mark.django_db
def test_login_wrong_password(form_data):
    client = Client()
    username = form_data['username']
    password = form_data['password']
    user = CustomUser.objects.create_user(username=username, password=password)
    url = reverse('login')
    response = client.post(url, {'username': username, 'password': 'wrong'})
    assert response.status_code != 302, "Expected no redirect after unsuccessful login"


@pytest.mark.django_db
def test_login_wrong_username(form_data):
    client = Client()
    username = form_data['username']
    password = form_data['password']
    user = CustomUser.objects.create_user(username=username, password=password)
    url = reverse('login')
    response = client.post(url, {'username': 'wrong', 'password': password})
    assert response.status_code != 302, "Expected no redirect after unsuccessful login"


@pytest.mark.urls('task_manager.urls')
def test_user_edit_no_auth(user, form_data):
    client = Client()
    url = reverse('users:users_update', kwargs={'user_id': user.id})
    with transaction.atomic():
        CustomUser.objects.filter(username=form_data['username']).delete()
    response = client.post(url, data=form_data, follow=True)
    assert response.status_code == 200
    assert 'login' in response.request['PATH_INFO'].lower()
    assert not CustomUser.objects.filter(username=form_data['username']).exists()


@pytest.mark.urls('task_manager.urls')
def test_cannot_change_another_users_data(user, another_user, form_data):
    client = Client()
    client.force_login(user)
    url = reverse('users:users_update', kwargs={'user_id': another_user.id})
    response = client.post(url, data=form_data, follow=True)
    assert response.redirect_chain[-1][0] == reverse(
        'users:users'), "Пользователь не был перенаправлен на ожидаемую страницу"
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0, "Сообщение об ошибке не было добавлено"
    assert "У вас нет прав для изменения другого пользователя." in str(messages[0]), "Неверное сообщение об ошибке"


@pytest.mark.urls('task_manager.urls')
def test_can_edit_own_data(user, form_data):
    client = Client()
    client.force_login(user)
    original_name = user.name
    original_surname = user.surname
    url = reverse('users:users_update', kwargs={'user_id': user.id})
    response = client.post(url, data=form_data, follow=True)
    assert response.status_code == 200
    updated_user = CustomUser.objects.get(id=user.id)
    new_name = updated_user.name
    new_surname = updated_user.surname
    assert new_name != original_name, "Имя пользователя не было обновлено"
    assert new_surname != original_surname, "Фамилия пользователя не была обновлена"
    assert new_name == form_data['name'], "Имя пользователя не совпадает с отправленным"
    assert new_surname == form_data['surname'], "Фамилия пользователя не совпадает с отправленной"


@pytest.mark.urls('task_manager.urls')
def test_cannot_save_invalid_data(user, invalid_form_data):
    client = Client()
    client.force_login(user)
    action_url = reverse('users:users_update', kwargs={'user_id': user.id})
    response = client.post(action_url, data=invalid_form_data, follow=True)
    assert response.status_code == 200
    updated_user = CustomUser.objects.get(id=user.id)
    assert updated_user.name == user.name, "Имя пользователя должно остаться неизменным"
    assert updated_user.surname == user.surname, "Фамилия пользователя должна остаться неизменной"


@pytest.mark.urls('task_manager.urls')
def test_user_edit_no_auth(user):
    client = Client()
    url = reverse('users:users_confirm_delete', kwargs={'user_id': user.id})
    response = client.get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)
    assert CustomUser.objects.filter(id=user.id).exists()
    with transaction.atomic():
        CustomUser.objects.filter(id=user.id).delete()