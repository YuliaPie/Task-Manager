from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Label
from .forms import LabelForm
from django.urls import reverse_lazy
from task_manager.tools import AuthRequiredMixin, DeleteProtectMixin
from django.utils.translation import gettext as _


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'labels/labels_list.html'


class LabelCreateView(AuthRequiredMixin,
                      SuccessMessageMixin,
                      CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _("Label successfully created")


class LabelEditView(SuccessMessageMixin,
                    AuthRequiredMixin,
                    UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _("Label changed successfully")


class LabelDeleteView(SuccessMessageMixin,
                      DeleteProtectMixin,
                      AuthRequiredMixin,
                      DeleteView):
    model = Label
    success_url = reverse_lazy('labels:labels')
    protected_message = _("Cannot delete label because it is in use")
    protected_url = reverse_lazy('labels:labels')
    template_name = 'labels/label_confirm_delete.html'
    success_message = _("Label successfully deleted")
