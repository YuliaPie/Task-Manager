import pytest
from ..statuses.models import Status
from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages


@pytest.mark.urls('task_manager.urls')
def test_get_statuses_list(authenticated_client):
    url = reverse('statuses:statuses')
    response = authenticated_client.get(url)
    assert response.status_code == 200


@pytest.mark.urls('task_manager.urls')
def test_get_statuses_list_unauthorised(user):
    url = reverse('statuses:statuses')
    response = Client().get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_create_status(authenticated_client, status_form_data):
    url = reverse('statuses:statuses_create')
    response = authenticated_client.post(url,
                                         data=status_form_data, follow=True)
    assert response.status_code == 200
    assert Status.objects.filter(name=status_form_data['name']).exists()


@pytest.mark.urls('task_manager.urls')
def test_create_status_unauthorised(user):
    client = Client()
    url = reverse('statuses:statuses_create')
    response = client.get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_create_status_same_data(authenticated_client, status_form_data):
    url = reverse('statuses:statuses_create')
    authenticated_client.post(url, data=status_form_data, follow=True)
    response = authenticated_client.post(url,
                                         data=status_form_data, follow=True)
    assert response.status_code != 302
    name_to_check = status_form_data['name']
    statuses_count = Status.objects.filter(name=name_to_check).count()
    assert statuses_count == 1


@pytest.mark.urls('task_manager.urls')
def test_get_statuses_upd_page_unauthorised(user, status):
    client = Client()
    url = reverse('statuses:statuses_update', kwargs={'pk': status.pk})
    response = client.get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_get_statuses_upd_page(authenticated_client, status):
    url = reverse('statuses:statuses_update', kwargs={'pk': status.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0, "Сообщение об ошибке было добавлено"


@pytest.mark.urls('task_manager.urls')
def test_upd_status(authenticated_client, status, status_form_data):
    original_name = status.name
    url = reverse('statuses:statuses_update', kwargs={'pk': status.pk})
    response = authenticated_client.post(url,
                                         data=status_form_data, follow=True)
    assert response.status_code == 200
    updated_status = Status.objects.get(pk=status.pk)
    new_name = updated_status.name
    assert new_name != original_name, "Название статуса не было обновлено"
    assert new_name == status_form_data['name'], \
        "Название статуса не совпадает с отправленным"


@pytest.mark.urls('task_manager.urls')
def test_upd_inv_data(authenticated_client, status, status_form_data):
    original_name = status.name
    Status.objects.create_status(name=status_form_data['name'])
    url = reverse('statuses:statuses_update', kwargs={'pk': status.pk})
    response = authenticated_client.post(url,
                                         data=status_form_data, follow=True)
    assert response.status_code == 200
    updated_status = Status.objects.get(pk=status.pk)
    assert updated_status.name == original_name, \
        "Имя пользователя должно остаться неизменным"


@pytest.mark.urls('task_manager.urls')
def test_get_del_page_unauthorised(status):
    client = Client()
    url = reverse('statuses:statuses_delete',
                  kwargs={'pk': status.pk})
    response = client.get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_get_status_del_page(authenticated_client, status):
    url = reverse('statuses:statuses_delete',
                  kwargs={'pk': status.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0, "Сообщение об ошибке было добавлено"


@pytest.mark.django_db(transaction=True)
def test_can_delete_status(authenticated_client, status):
    url = reverse('statuses:statuses_delete', kwargs={'pk': status.pk})
    authenticated_client.post(url)
    deleted_status = Status.objects.filter(pk=status.pk)
    assert not deleted_status.exists(), "Статус не был удален"
