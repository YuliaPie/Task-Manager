from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (UpdateView, CreateView,
                                  DeleteView, ListView)

from task_manager.tools import (AuthRequiredMixin,
                                UserPermissionMixin,
                                DeleteProtectMixin)
from .forms import UserForm
from .models import CustomUser
import logging
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class UserListView(ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'users/user_list.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = _("The user has been registered successfully.")
    extra_context = {
        'title': _("Registration"),
        'submit_button_text': _("Register"),
    }


class UserUpdateView(SuccessMessageMixin,
                     AuthRequiredMixin,
                     UserPermissionMixin,
                     UserPassesTestMixin,
                     UpdateView
                     ):
    model = CustomUser
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('users:users')
    success_message = _("User successfully changed")
    extra_context = {
        'title': _("Edit user"),
        'submit_button_text': _("Edit"),
    }


class UserDeleteView(SuccessMessageMixin,
                     DeleteProtectMixin,
                     AuthRequiredMixin,
                     UserPermissionMixin,
                     UserPassesTestMixin,
                     DeleteView,
                     ):
    model = CustomUser
    success_url = reverse_lazy('users:users')
    protected_message = _("Cannot delete user because it is in use")
    protected_url = reverse_lazy('users:users')
    template_name = 'delete.html'
    success_message = _("User successfully deleted")
    extra_context = {
        'title': _("Delete user"),
        'submit_button_text': _("Yes, delete"),
    }
