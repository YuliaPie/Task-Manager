from django.urls import path
from task_manager.users.views import (UserListView,
                                      UserCreateView,
                                      UserUpdateView,
                                      UserDeleteView)


app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='users_create'),
    path('<int:pk>/update/',
         UserUpdateView.as_view(),
         name='users_update'),
    path('delete/<int:pk>/',
         UserDeleteView.as_view(), name='users_delete'),
]
