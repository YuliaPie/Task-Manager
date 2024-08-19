import pytest
from ..labels.models import Label
from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages


@pytest.mark.urls('task_manager.urls')
def test_get_labels_list(authenticated_client):
    url = reverse('labels:labels')
    response = authenticated_client.get(url)
    assert response.status_code == 200


@pytest.mark.urls('task_manager.urls')
def test_get_labels_list_unauthorised(user):
    url = reverse('labels:labels')
    response = Client().get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_create_label(authenticated_client, label_form_data):
    url = reverse('labels:labels_create')
    response = authenticated_client.post(url,
                                         data=label_form_data, follow=True)
    assert response.status_code == 200
    assert Label.objects.filter(name=label_form_data['name']).exists()


@pytest.mark.urls('task_manager.urls')
def test_create_label_unauthorised(user):
    client = Client()
    url = reverse('labels:labels_create')
    response = client.get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_create_label_same_data(authenticated_client, label_form_data):
    url = reverse('labels:labels_create')
    authenticated_client.post(url, data=label_form_data, follow=True)
    response = authenticated_client.post(url,
                                         data=label_form_data, follow=True)
    assert response.status_code != 302
    name_to_check = label_form_data['name']
    labels_count = Label.objects.filter(name=name_to_check).count()
    assert labels_count == 1


@pytest.mark.urls('task_manager.urls')
def test_get_labels_upd_page_unauthorised(user, label):
    client = Client()
    url = reverse('labels:labels_update', kwargs={'pk': label.pk})
    response = client.get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_get_labels_upd_page(authenticated_client, label):
    url = reverse('labels:labels_update', kwargs={'pk': label.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0, "Сообщение об ошибке было добавлено"


@pytest.mark.urls('task_manager.urls')
def test_upd_label(authenticated_client, label, label_form_data):
    original_name = label.name
    url = reverse('labels:labels_update', kwargs={'pk': label.pk})
    response = authenticated_client.post(url,
                                         data=label_form_data, follow=True)
    assert response.status_code == 200
    updated_label = Label.objects.get(pk=label.pk)
    new_name = updated_label.name
    assert new_name != original_name, "Название статуса не было обновлено"
    assert new_name == label_form_data['name'], \
        "Название метки не совпадает с отправленным"


@pytest.mark.urls('task_manager.urls')
def test_upd_inv_data(authenticated_client, label, label_form_data):
    original_name = label.name
    Label.objects.create_label(name=label_form_data['name'])
    url = reverse('labels:labels_update', kwargs={'pk': label.pk})
    response = authenticated_client.post(url,
                                         data=label_form_data, follow=True)
    assert response.status_code == 200
    updated_label = Label.objects.get(pk=label.pk)
    assert updated_label.name == original_name, \
        "Имя метки должно остаться неизменным"


@pytest.mark.urls('task_manager.urls')
def test_get_del_page_unauthorised(label):
    client = Client()
    url = reverse('labels:labels_delete',
                  kwargs={'pk': label.pk})
    response = client.get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_get_label_del_page(authenticated_client, label):
    url = reverse('labels:labels_delete',
                  kwargs={'pk': label.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0, "Сообщение об ошибке было добавлено"


@pytest.mark.django_db(transaction=True)
def test_can_delete_label(authenticated_client, label):
    pk = label.pk
    url = reverse('labels:labels_delete', kwargs={'pk': label.pk})
    authenticated_client.post(url)
    deleted_label = Label.objects.filter(pk=pk)
    assert not deleted_label.exists(), "Метка не была удалена"
