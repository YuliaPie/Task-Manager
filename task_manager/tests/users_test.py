import pytest
from ..users.models import CustomUser
from .conftest import authenticated_client, form_data, user
from django.test import Client
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.db import transaction
from ..users.forms import UserForm


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
