from django.contrib.auth.views import redirect_to_login
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from .forms import UserForm
from django.shortcuts import redirect, render
from django.contrib import messages


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        return render(request, 'users/user_list.html', context={
            'users': users,
        })


class UserFormCreateView(View):

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно зарегистрирован", extra_tags='success')
            return redirect('users:users')
        else:
            messages.error(request, "Проверьте введенные данные", extra_tags='danger')
            return render(request, 'users/create.html', {'form': form})


class UserFormEditView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Вы не авторизованы! Пожалуйста, выполните вход.", extra_tags='danger')
            return redirect_to_login(request.path, '/login/', 'next')
        username = kwargs.get('username')
        if request.user.username != username:
            messages.error(request, "Вы не имеете права редактировать чужую учетную запись.", extra_tags='danger')
            return redirect('users:users')

        user = get_object_or_404(CustomUser, username=username)
        form = UserForm(instance=user)
        return render(request, 'users/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Вы не авторизованы! Пожалуйста, выполните вход.", extra_tags='danger')
            return redirect_to_login(request.path, '/login/', 'next')

        username = kwargs.get('username')
        if request.user.username != username:
            messages.error(request, "Вы не авторизованы! Пожалуйста, выполните вход.", extra_tags='danger')
            return redirect('login')

        user = get_object_or_404(CustomUser, username=username)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password'))
            form.save()
            messages.success(request, "Пользователь успешно изменен", extra_tags='success')
            return redirect('users:users')
        messages.error(request, "Ошибка в форме", extra_tags='danger')
        return render(request, 'users/update.html', {'form': form})


def user_confirm_delete(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user.id != user.id:
        messages.error(request, "Вы не авторизованы! Пожалуйста, выполните вход.", extra_tags='danger')
        return redirect_to_login(request.path, '/login/', 'next')  # Используем 'next' для перенаправления после входа

    return render(request, 'users/user_confirm_delete.html', {'user': user})


def user_delete(request, user_id):
    if not request.user.is_authenticated:
        request.session['auth_error_message'] = "Вы не авторизованы! Пожалуйста, выполните вход."
        return redirect_to_login(request.path, '/login/', 'next')
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user.id != user.id:
        messages.error(request, "У вас нет прав для изменения другого пользователя.", extra_tags='danger')
        return redirect('users:users')

    user.delete()
    messages.success(request, "Пользователь успешно удален.")
    return redirect('users:users')