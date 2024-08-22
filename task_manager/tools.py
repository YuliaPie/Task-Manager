from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class AuthRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("You are not logged in! Please sign in."),
                extra_tags='danger')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin:
    def test_func(self):
        if self.request.user.pk != self.get_object().pk:
            return False
        return True

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You do not have permission to modify another user."),
            extra_tags='danger')
        return HttpResponseRedirect(reverse_lazy('users:users'))


class DeleteProtectMixin:
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message,
                           extra_tags='danger')
            return redirect(self.protected_url)


class AuthorPermissionMixin:
    def test_func(self):
        if self.request.user.pk != self.get_object().author.pk:
            return False
        return True

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("A task can only be deleted by its author"),
            extra_tags='danger')
        return redirect('tasks:tasks')
