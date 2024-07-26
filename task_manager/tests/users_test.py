import pytest
from django.urls import reverse
from ..users.models import CustomUser
from .conftest import authenticated_client, form_data, user
from django.contrib.auth.hashers import check_password


@pytest.mark.urls('task_manager.urls')
def test_user_create_valid_data(authenticated_client, form_data, user,
                                          db):
    CustomUser.objects.filter(username=user.username).delete()
    url = reverse('users:users_create')
    response = authenticated_client.post(url, data=form_data)
    assert response.status_code == 302
    created_user = CustomUser.objects.get(username='testuser')
    assert created_user.username == form_data['username']
    assert check_password(form_data['password'], created_user.password)
    assert created_user.name == form_data['name']
    assert created_user.surname == form_data['surname']