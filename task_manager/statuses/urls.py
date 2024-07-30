from django.urls import path
from task_manager.statuses.views import (IndexView, StatusFormCreateView,
                                      StatusFormEditView,
                                      status_confirm_delete,
                                      StatusDeleteView)


app_name = 'statuses'

urlpatterns = [
    path('', IndexView.as_view(), name='statuses'),
    path('create/', StatusFormCreateView.as_view(), name='statuses_create'),
    path('<int:status_id>/update/',
         StatusFormEditView.as_view(),
         name='statuses_update'),
    path('<int:status_id>/delete/',
         status_confirm_delete,
         name='status_confirm_delete'),
    path('delete/<int:status_id>/', StatusDeleteView.as_view(), name='statuses_delete'),
]
