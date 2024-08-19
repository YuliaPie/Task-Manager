from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView,
                                  UpdateView,
                                  DeleteView,
                                  ListView)
from .models import Status
from .forms import StatusForm
from django.urls import reverse_lazy
from task_manager.tools import AuthRequiredMixin


class StatusListView(AuthRequiredMixin, ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/status_list.html'


class StatusCreateView(AuthRequiredMixin,
                       SuccessMessageMixin,
                       CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = "Статус успешно создан"


class StatusEditView(AuthRequiredMixin,
                     UpdateView,
                     SuccessMessageMixin):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = "Статус успешно изменен"


class StatusDeleteView(AuthRequiredMixin,
                       DeleteView,
                       SuccessMessageMixin):
    model = Status
    success_url = reverse_lazy('statuses:statuses')
    template_name = 'statuses/status_confirm_delete.html'
    success_message = "Статус успешно удален."
