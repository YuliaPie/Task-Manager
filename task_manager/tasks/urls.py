from django.urls import path
from task_manager.tasks.views import (IndexView, TaskFormCreateView,
                                      TaskFormEditView,
                                      task_confirm_delete,
                                      TaskDeleteView,
                                      task_info)


app_name = 'tasks'

urlpatterns = [
    path('', IndexView.as_view(), name='tasks'),
    path('create/', TaskFormCreateView.as_view(), name='tasks_create'),
    path('<int:task_id>/update/',
         TaskFormEditView.as_view(),
         name='task_update'),
    path('<int:task_id>/delete/',
         task_confirm_delete,
         name='task_confirm_delete'),
    path('delete/<int:task_id>/', TaskDeleteView.as_view(), name='tasks_delete'),
    path('<int:task_id>/',
         task_info,
         name='task_info'),
]
