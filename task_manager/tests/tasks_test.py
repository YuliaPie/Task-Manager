import pytest
from ..tasks.models import Task
from django.test import Client
from django.urls import reverse
import logging
from django.contrib.messages import get_messages


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@pytest.mark.urls('task_manager.urls')
def test_get_task_list(authenticated_client):
    url = reverse('tasks:tasks')
    response = authenticated_client.get(url)
    assert response.status_code == 200


@pytest.mark.urls('task_manager.urls')
def test_task_filter(authenticated_client, user, task, task1, task2, label):
    url = reverse('tasks:tasks')
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert len(response.context['tasks']) == 3
    response = authenticated_client.get(url, {'status': task.status.id})
    assert response.status_code == 200
    assert len(response.context['tasks']) == 2
    assert response.context['tasks'][0].id == task.id
    authenticated_client.login(username=user.username,
                               password=user. password)
    response = authenticated_client.get(url, {'self_tasks': 'true'})
    assert response.status_code == 200
    assert len(response.context['tasks']) == 2
    assert set(task.id for task in
               response.context['tasks']) == {task.id, task2.id}
    response = authenticated_client.get(url, {'label': label.id})
    assert response.status_code == 200
    assert len(response.context['tasks']) == 2
    assert set(task.id for task in
               response.context['tasks']) == {task.id, task1.id}


@pytest.mark.urls('task_manager.urls')
def test_get_task_list_unauthorised(db):
    url = reverse('tasks:tasks')
    response = Client().get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_create_task(db, authenticated_client, task_form_data):
    url = reverse('tasks:tasks_create')
    response = authenticated_client.post(url, task_form_data, follow=False)
    assert response.status_code == 302
    assert Task.objects.filter(name=task_form_data['name']).exists()


@pytest.mark.urls('task_manager.urls')
def test_create_task_unauthorised(db):
    url = reverse('tasks:tasks_create')
    response = Client().get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_create_task_same_data(authenticated_client, task_form_data):
    url = reverse('tasks:tasks_create')
    authenticated_client.post(url, data=task_form_data, follow=True)
    response = authenticated_client.post(url, data=task_form_data, follow=True)
    assert response.status_code != 302
    name_to_check = task_form_data['name']
    statuses_count = Task.objects.filter(name=name_to_check).count()
    assert statuses_count == 1


@pytest.mark.urls('task_manager.urls')
def test_get_task_upd_page_unauthorised(user, task):
    client = Client()
    url = reverse('tasks:task_update', kwargs={'task_id': task.id})
    response = client.get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_get_task_upd_page(authenticated_client, task):
    url = reverse('tasks:task_update', kwargs={'task_id': task.id})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0, "Сообщение об ошибке было добавлено"


@pytest.mark.urls('task_manager.urls')
def test_upd_task(authenticated_client, task):
    original_name = task.name
    url = reverse('tasks:task_update', kwargs={'task_id': task.id})
    new_name = 'New name'
    labels_ids = task.labels.values_list('id', flat=True)
    response = authenticated_client.post(url, data={
        'name': new_name,
        'description': task.description,
        'status': 1,
        'labels': labels_ids,
    }, follow=True)
    assert response.status_code == 200
    logger.info(f"Server response: {response.content.decode()}")
    updated_task = Task.objects.get(id=task.id)
    assert updated_task.name != original_name, \
        "Название задачи не было обновлено"
    assert updated_task.name == new_name, \
        "Название задачи не совпадает с отправленным"


@pytest.mark.urls('task_manager.urls')
def test_upd_inv_data(authenticated_client, task):
    original_name = task.name
    url = reverse('tasks:task_update', kwargs={'task_id': task.id})
    new_name = 'New name'
    response = authenticated_client.post(url, data={
        'author': task.author.id,
        'name': new_name,
        'description': task.description,
        'status': ""
    }, follow=True)
    assert response.status_code == 200
    updated_task = Task.objects.get(id=task.id)
    assert updated_task.name == original_name, \
        "Имя задачи должно остаться неизменным"


@pytest.mark.urls('task_manager.urls')
def test_get_del_page_unauthorised(task):
    url = reverse('tasks:task_confirm_delete',
                  kwargs={'task_id': task.id})
    response = Client().get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_get_task_del_page(authenticated_client, task):
    url = reverse('tasks:task_confirm_delete',
                  kwargs={'task_id': task.id})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0, "Сообщение об ошибке было добавлено"


@pytest.mark.django_db(transaction=True)
def test_can_delete_task(authenticated_client, task):
    id = task.id
    url = reverse('tasks:tasks_delete', kwargs={'task_id': task.id})
    authenticated_client.post(url)
    deleted_task = Task.objects.filter(id=id)
    assert not deleted_task.exists(), "Задача не была удалена"


@pytest.mark.urls('task_manager.urls')
def test_get_info_page_unauthorised(task):
    url = reverse('tasks:task_info',
                  kwargs={'task_id': task.id})
    response = Client().get(url)
    assert response.status_code == 302
    next_url = response.url
    login_url = reverse('login')
    assert next_url.startswith(login_url)


@pytest.mark.urls('task_manager.urls')
def test_get_task_info_page(authenticated_client, task):
    url = reverse('tasks:task_info',
                  kwargs={'task_id': task.id})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0, "Сообщение об ошибке было добавлено"
