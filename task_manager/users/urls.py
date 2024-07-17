from django.urls import path
from task_manager.users.views import (IndexView, UserFormCreateView,
                                      UserFormEditView,
                                      user_confirm_delete,
                                      user_delete)


app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='users'),
    path('create/', UserFormCreateView.as_view(), name='users_create'),
    path('<int:pk>/update/', UserFormEditView.as_view(), name='users_update'),
    path('<int:user_id>/delete/', user_confirm_delete, name='users_confirm_delete'),
    path('<int:user_id>/delete/', user_delete, name='users_delete'),
]
