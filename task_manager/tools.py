from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from task_manager.forms import LoginForm


def check_and_redirect_if_not_auth(request):
    if not request.user.is_authenticated:
        messages.error(
            request,
            "Вы не авторизованы! "
            "Пожалуйста, выполните вход.", extra_tags='danger')
        return redirect('login')
    return None


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
