import pytest
from ..users.models import CustomUser
from django.test import Client
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.contrib.messages import get_messages


@pytest.mark.urls('task_manager.urls')
def test_create_user(form_data, db):
    url = reverse('users:users_create')
    response = Client().post(url, data=form_data, follow=True)
    created_user = CustomUser.objects.get(username=form_data['username'])
    assert created_user.username == form_data['username']
    assert check_password(form_data['password1'], created_user.password)
    assert created_user.first_name == form_data['first_name']
    assert created_user.last_name == form_data['last_name']
    messages = get_messages(response.wsgi_request)
    success_message = "Пользователь успешно зарегистрирован."
    assert (
        any(
            message.message == success_message
            for message
            in messages)), \
        "Сообщение об успехе отсутствует"


@pytest.mark.urls('task_manager.urls')
def test_create_user_inv_data(invalid_form_data, db):
    client = Client()
    url = reverse('users:users_create')
    response = client.post(url, data=invalid_form_data)
    assert response.status_code != 302
    username_to_check = invalid_form_data['username']
    users_count = CustomUser.objects.filter(username=username_to_check).count()
    assert users_count == 0


@pytest.mark.django_db
def test_login(form_data):
    client = Client()
    username = form_data['username']
    password = form_data['password1']
    CustomUser.objects.create_user(username=username, password=password)
    url = reverse('login')
    response = client.post(url, {'username': username, 'password': password})
    assert response.status_code == 302, \
        "Expected redirect after successful login"


@pytest.mark.django_db
def test_login_wrong_password(form_data):
    client = Client()
    username = form_data['username']
    password = form_data['password1']
    CustomUser.objects.create_user(username=username, password=password)
    url = reverse('login')
    response = client.post(url, {'username': username, 'password': 'wrong'})
    assert response.status_code != 302, \
        "Expected no redirect after unsuccessful login"


@pytest.mark.django_db
def test_login_wrong_username(form_data):
    client = Client()
    username = form_data['username']
    password = form_data['password1']
    CustomUser.objects.create_user(username=username, password=password)
    url = reverse('login')
    response = client.post(url, {'username': 'wrong', 'password': password})
    assert response.status_code != 302, \
        "Expected no redirect after unsuccessful login"


@pytest.mark.urls('task_manager.urls')
def test_get_upd_page_unauthorised(user, form_data):
    client = Client()
    url = reverse('users:users_update', kwargs={'pk': user.pk})
    with transaction.atomic():
        CustomUser.objects.filter(username=form_data['username']).delete()
    response = client.post(url, data=form_data, follow=True)
    assert response.status_code == 200
    assert 'login' in response.request['PATH_INFO'].lower()
    assert not (
        CustomUser.objects.filter(username=form_data['username']).exists())


@pytest.mark.urls('task_manager.urls')
def test_upd_another_user(authenticated_client, another_user, form_data):
    url = reverse('users:users_update', kwargs={'pk': another_user.pk})
    response = authenticated_client.post(url, data=form_data, follow=True)
    assert response.redirect_chain[-1][0] == reverse(
        'users:users'), ("Пользователь не был "
                         "перенаправлен на ожидаемую страницу")
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0, "Сообщение об ошибке не было добавлено"
    assert ("У вас нет прав для изменения другого пользователя."
            in str(messages[0])), "Неверное сообщение об ошибке"


@pytest.mark.urls('task_manager.urls')
def test_get_another_user_upd_page(authenticated_client, another_user):
    url = reverse('users:users_update', kwargs={'pk': another_user.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('users:users'), \
        "Пользователь не был перенаправлен на ожидаемую страницу"
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0, "Сообщение об ошибке не было добавлено"
    assert ("У вас нет прав для изменения "
            "другого пользователя.") in str(messages[0]), \
        "Неверное сообщение об ошибке"


@pytest.mark.urls('task_manager.urls')
def test_get_own_upd_page(authenticated_client, user):
    url = reverse('users:users_update', kwargs={'pk': user.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0, "Сообщение об ошибке было добавлено"


@pytest.mark.urls('task_manager.urls')
def test_upd_user(authenticated_client, user, form_data):
    original_first_name = user.first_name
    original_last_name = user.last_name
    url = reverse('users:users_update', kwargs={'pk': user.pk})
    response = authenticated_client.post(url, data=form_data, follow=True)
    assert response.status_code == 200
    updated_user = CustomUser.objects.get(id=user.id)
    new_first_name = updated_user.first_name
    new_last_name = updated_user.last_name
    assert (new_first_name
            != original_first_name), \
        "Имя пользователя не было обновлено"
    assert (new_last_name
            != original_last_name), \
        "Фамилия пользователя не была обновлена"
    assert (new_first_name
            == form_data['first_name']), \
        "Имя пользователя не совпадает с отправленным"
    assert (new_last_name
            == form_data['last_name']), \
        "Фамилия пользователя не совпадает с отправленной"
    """
    messages = get_messages(response.wsgi_request)
    success_message = "Пользователь успешно изменен."
    assert any(message.message
               == success_message
               for message
               in messages), "Сообщение об успехе отсутствует"
    """


@pytest.mark.urls('task_manager.urls')
def test_upd_inv_data(user, invalid_form_data):
    client = Client()
    client.force_login(user)
    action_url = reverse('users:users_update', kwargs={'pk': user.pk})
    response = client.post(action_url, data=invalid_form_data, follow=True)
    assert response.status_code == 200
    updated_user = CustomUser.objects.get(id=user.id)
    assert updated_user.first_name == user.first_name, \
        "Имя пользователя должно остаться неизменным"
    assert updated_user.last_name == user.last_name, \
        "Фамилия пользователя должна остаться неизменной"


@pytest.mark.urls('task_manager.urls')
def test_get_del_page_unauthorised(user):
    client = Client()
    url = reverse('users:users_delete', kwargs={'pk': user.pk})
    response = client.get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_get_del_page_another_user(authenticated_client, another_user):
    url = reverse('users:users_delete',
                  kwargs={'pk': another_user.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('users:users'), \
        "Пользователь не был перенаправлен на ожидаемую страницу"
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0, "Сообщение об ошибке не было добавлено"
    assert ("У вас нет прав для изменения другого пользователя."
            in str(messages[0])), "Неверное сообщение об ошибке"


@pytest.mark.urls('task_manager.urls')
def test_get_own_del_page(authenticated_client, user):
    url = reverse('users:users_delete', kwargs={'pk': user.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0, "Сообщение об ошибке было добавлено"


@pytest.mark.django_db(transaction=True)
def test_user_can_delete_own_account(authenticated_client, user):
    url = reverse('users:users_delete', kwargs={'pk': user.pk})
    authenticated_client.post(url)
    with transaction.atomic():
        assert not CustomUser.objects.filter(
            pk=user.pk).exists(), "Пользователь не был удален"
