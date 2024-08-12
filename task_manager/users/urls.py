from django.urls import path
from task_manager.users.views import (IndexView, UserCreateView,
                                      UserUpdateView,
                                      user_confirm_delete,
                                      UserDeleteView)


app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='users'),
    path('create/',UserCreateView.as_view(), name='users_create'),
    path('update/<int:pk>/',
         UserUpdateView.as_view(),
         name='users_update'),
    path('<int:user_id>/delete/',
         user_confirm_delete,
         name='users_confirm_delete'),
    path('delete/<int:user_id>/',
         UserDeleteView.as_view(), name='users_delete'),
]
