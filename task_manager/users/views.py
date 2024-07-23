from task_manager.users.models import CustomUser
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from task_manager.users.forms import UserForm


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
        username = kwargs.get('username')
        article = CustomUser.objects.get(username=user_username)
        form = UserForm(instance=article)
        return render(request, 'users/update.html',
                      {'form': form, 'user_id': user_id})

    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = CustomUser.objects.get(id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password'))
            form.save()
            messages.success(request, "Пользователь успешно изменен", extra_tags='success')
            return redirect('user:user')
        messages.error(request, "Ошибка в форме", extra_tags='danger')
        return render(request, 'users/update.html',
                      {'form': form, 'user_id': user_id})


def user_confirm_delete(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'users/user_confirm_delete.html', {'user': user})


def user_delete(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    messages.success(request, "Пользователь успешно удален.")
    return redirect('users_list')