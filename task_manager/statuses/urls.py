from django.urls import path
from task_manager.statuses.views import (StatusListView, StatusCreateView,
                                         StatusEditView,
                                         StatusDeleteView)


app_name = 'statuses'

urlpatterns = [
    path('', StatusListView.as_view(),
         name='statuses'),
    path('create/', StatusCreateView.as_view(),
         name='statuses_create'),
    path('<int:pk>/update/',
         StatusEditView.as_view(),
         name='statuses_update'),
    path('<int:pk>/delete/',
         StatusDeleteView.as_view(),
         name='statuses_delete'),
]
