from django.urls import path
from task_manager.labels.views import (LabelListView,
                                       LabelCreateView,
                                       LabelEditView,
                                       LabelDeleteView)

app_name = 'labels'

urlpatterns = [
    path('', LabelListView.as_view(), name='labels'),
    path('create/', LabelCreateView.as_view(), name='labels_create'),
    path('<int:pk>/update/',
         LabelEditView.as_view(),
         name='labels_update'),
    path('<int:pk>/delete/',
         LabelDeleteView.as_view(),
         name='labels_delete'),
]
