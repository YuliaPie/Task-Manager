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
    template_name = 'form.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _("Label successfully created")
    extra_context = {
        'title': _("Create labels"),
        'submit_button_text': _("Create"),
    }


class LabelEditView(SuccessMessageMixin,
                    AuthRequiredMixin,
                    UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _("Label changed successfully")
    extra_context = {
        'title': _("Edit label"),
        'submit_button_text': _("Edit"),
    }


class LabelDeleteView(SuccessMessageMixin,
                      DeleteProtectMixin,
                      AuthRequiredMixin,
                      DeleteView):
    model = Label
    success_url = reverse_lazy('labels:labels')
    protected_message = _("Cannot delete label because it is in use")
    protected_url = reverse_lazy('labels:labels')
    template_name = 'delete.html'
    success_message = _("Label successfully deleted")
    extra_context = {
        'title': _("Delete label"),
        'submit_button_text': _("Yes, delete"),
    }
