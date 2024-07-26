from django.contrib.auth.views import redirect_to_login
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from .forms import UserForm
from django.contrib import messages
from django.urls import reverse


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        return render(request, 'users/user_list.html', context={
            'users': users,
        })


class UserFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        action_url = reverse('users:users_create')
        return render(request,
                      'users/create.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        action_url = reverse('users:users_create')
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.save()
            messages.success(request,
                             "Пользователь успешно зарегистрирован",
                             extra_tags='success')
            return redirect('main_page')
        else:
            messages.error(request, None, extra_tags='danger')
            return render(request,
                          'users/create.html',
                          {'form': form, 'action_url': action_url})


class UserFormEditView(View):
    def get(self, request, user_id):
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        user = get_object_or_404(CustomUser, id=user_id)
        if request.user.id != user.id:
            messages.error(request,
                           "У вас нет прав для "
                           "изменения другого пользователя.",
                           extra_tags='danger')
            return redirect('users:users')
        form = UserForm(instance=user)
        form.initial['password'] = ''
        form.initial['password2'] = ''
        action_url = reverse('users:users_update', kwargs={'user_id': user.id})
        return render(request,
                      'users/update.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, user_id):
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path, '/login/', 'next')
        user = get_object_or_404(CustomUser, id=user_id)
        if request.user.id != user.id:
            messages.error(request,
                           "У вас нет прав для"
                           " изменения другого пользователя.",
                           extra_tags='danger')
            return redirect('users:users')
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password'))
            form.save()
            messages.success(request,
                             "Пользователь успешно изменен",
                             extra_tags='success')
            return redirect('users:users')
        action_url = reverse('users:users_update', kwargs={'user_id': user.id})
        messages.error(request, None, extra_tags='danger')
        return render(request,
                      'users/update.html',
                      {'form': form,
                       'action_url': action_url})


def user_confirm_delete(request, user_id):
    if not request.user.is_authenticated:
        messages.error(request,
                       "Вы не авторизованы! Пожалуйста, выполните вход.",
                       extra_tags='danger')
        return redirect_to_login(request.path, '/login/', 'next')
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user.id != user.id:
        messages.error(request,
                       "У вас нет прав для изменения другого пользователя.",
                       extra_tags='danger')
        return redirect(
            'users:users')
    return render(request, 'users/user_confirm_delete.html', {'user': user})


def user_delete(request, user_id):
    if not request.user.is_authenticated:
        request.session['auth_error_message'] =\
            "Вы не авторизованы! Пожалуйста, выполните вход."
        return redirect_to_login(request.path, '/login/', 'next')
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user.id != user.id:
        messages.error(request,
                       "У вас нет прав для изменения другого пользователя.",
                       extra_tags='danger')
        return redirect('users:users')

    user.delete()
    messages.success(request, "Пользователь успешно удален.")
    return redirect('users:users')
