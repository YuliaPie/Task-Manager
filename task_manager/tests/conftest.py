import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


@pytest.fixture
def user(db):
    CustomUserModel = get_user_model()
    user = CustomUserModel.objects.create_user(username='testuser',
                                               password='testpass')
    return user


@pytest.fixture
def another_user(db):
    model = get_user_model()
    another_user = model.objects.create_user(username='anotheruser',
                                             password='anotherpass')
    return another_user


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture(params=[{'first_name': 'test_first_name',
                         'last_name': 'test_last_name',
                         'username': 'testuser',
                         'password1': 'testpassword',
                         'password2': 'testpassword'}])
def form_data(request):
    return request.param


@pytest.fixture(params=[{'first_name': 'ok', 'last_name': 'ok', 'username': '*bad',
                         'password1': '1', 'password2': '2'}])
def invalid_form_data(request):
    return request.param


@pytest.fixture(params=[{'name': 'ok'}])
def status_form_data(request):
    return request.param


@pytest.fixture
def status(db):
    status = Status.objects.create_status(name='test')
    return status


@pytest.fixture
def another_status(db):
    another_status = Status.objects.create_status(name='test1')
    return another_status


@pytest.fixture
def task_form_data(user, status, label):
    form_data = {
        'author': user.id,
        'name': 'Test Task',
        'description': 'This is a test task.',
        'status': status.id,
        'executor': user.id,
        'labels': [label.id]
    }
    return form_data


@pytest.fixture
def task(db, user, status, label):
    task = Task.objects.create_task(
        author=user,
        name='Test Task',
        description='Description of the test task',
        status=status,
        executor=user,
    )
    task.labels.set([label.id])
    return task


@pytest.fixture
def task1(db, another_user, status, label):
    task1 = Task.objects.create_task(
        author=another_user,
        name='Test Task1',
        description='Description of the test task1',
        status=status,
    )
    task1.labels.set([label.id])
    return task1


@pytest.fixture
def task2(db, user, another_status, another_label):
    task2 = Task.objects.create_task(
        author=user,
        name='Test Task1',
        description='Description of the test task2',
        status=another_status,
    )
    task2.labels.set([another_label.id])
    return task2


@pytest.fixture(params=[{'name': 'test_status_name'}])
def label_form_data(request):
    return request.param


@pytest.fixture
def label(db):
    label = Label.objects.create_label(name='test')
    return label


@pytest.fixture
def another_label(db):
    another_label = Label.objects.create_label(name='another_test')
    return another_label
