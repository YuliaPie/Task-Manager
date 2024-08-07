from django.urls import path
from task_manager.labels.views import (IndexView, LabelFormCreateView,
                                       LabelFormEditView,
                                       label_confirm_delete,
                                       LabelDeleteView)

app_name = 'labels'

urlpatterns = [
    path('', IndexView.as_view(), name='labels'),
    path('create/', LabelFormCreateView.as_view(), name='labels_create'),
    path('<int:label_id>/update/',
         LabelFormEditView.as_view(),
         name='labels_update'),
    path('<int:label_id>/delete/',
         label_confirm_delete,
         name='labels_confirm_delete'),
    path('delete/<int:label_id>/',
         LabelDeleteView.as_view(),
         name='labels_delete'),
]
