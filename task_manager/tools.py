from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from task_manager.forms import LoginForm
from task_manager.tasks.models import Task


def clear_session_username(request):
    try:
        del request.session['username']
    except KeyError:
        pass


def initialize_login_form_with_session(request):
    form = LoginForm()
    if 'username' in request.session:
        form.fields['username'].initial = request.session.get('username', '')
    return form


class AuthRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                "Вы не авторизованы! Пожалуйста, выполните вход.",
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
            "У вас нет прав для изменения другого пользователя.",
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
        obj = self.get_object()
        return obj.author == self.request.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Задачу может удалить только ее автор",
            extra_tags='danger')
        return redirect('tasks:tasks')
