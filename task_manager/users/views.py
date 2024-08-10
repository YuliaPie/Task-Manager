from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from .forms import UserForm
from django.urls import reverse
from django.contrib import messages
from task_manager.tools import check_and_redirect_if_not_auth


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
            new_user.set_password(form.cleaned_data.get('password1'))
            new_user.save()
            messages.success(request,
                             "Пользователь успешно зарегистрирован",
                             extra_tags='success')
            return redirect('login')
        else:
            messages.error(request, None, extra_tags='danger')
            return render(request,
                          'users/create.html',
                          {'form': form, 'action_url': action_url})


class UserFormEditView(View):
    def get(self, request, user_id):
        is_authorised = check_and_redirect_if_not_auth(request)
        if is_authorised:
            return is_authorised
        user = get_object_or_404(CustomUser, id=user_id)
        if request.user.id != user.id:
            messages.error(request,
                           "У вас нет прав для "
                           "изменения другого пользователя.",
                           extra_tags='danger')
            return redirect('users:users')
        form = UserForm(instance=user)
        form.initial['password1'] = None
        form.initial['password2'] = None
        action_url = reverse('users:users_update', kwargs={'user_id': user.id})
        return render(request,
                      'users/update.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, user_id):
        is_authorised = check_and_redirect_if_not_auth(request)
        if is_authorised:
            return is_authorised
        user = get_object_or_404(CustomUser, id=user_id)
        if request.user.id != user.id:
            messages.error(request,
                           "У вас нет прав для изменения другого пользователя.",
                           extra_tags='danger')
            return redirect('users:users')

        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password'))
            form.full_clean()
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
    is_authorised = check_and_redirect_if_not_auth(request)
    if is_authorised:
        return is_authorised
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user.id != user.id:
        messages.error(request,
                       "У вас нет прав для изменения другого пользователя.",
                       extra_tags='danger')
        return redirect(
            'users:users')
    return render(request, 'users/user_confirm_delete.html', {'user': user})


class UserDeleteView(View):

    def post(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        if user:
            user.delete()
        messages.success(request, "Пользователь успешно удален.")
        return redirect('users:users')
