from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView,
                                  UpdateView,
                                  DeleteView,
                                  ListView)
from .models import Status
from .forms import StatusForm
from django.urls import reverse_lazy
from task_manager.tools import AuthRequiredMixin, DeleteProtectMixin
from django.utils.translation import gettext as _


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
    success_message = _("Status successfully created")


class StatusEditView(AuthRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _("Status changed successfully")


class StatusDeleteView(SuccessMessageMixin,
                       DeleteProtectMixin,
                       AuthRequiredMixin,
                       DeleteView
                       ):
    model = Status
    success_url = reverse_lazy('statuses:statuses')
    protected_message = _("Cannot delete status because it is in use")
    protected_url = reverse_lazy('statuses:statuses')
    template_name = 'statuses/status_confirm_delete.html'
    success_message = _("Status successfully deleted")
