from django.shortcuts import render, redirect
from django.views import View
from task_manager.forms import LoginForm
from django.contrib.auth import authenticate, logout
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate_user(request, username, password)
            if user is not None:
                messages.success(request, "Вы залогинены", extra_tags='success')
                return redirect('main_page')
            else:
                messages.error(request, "Неверный логин или пароль", extra_tags='danger')
        return render(request, 'login.html', {'form': form})


def authenticate_user(request, username, password):
    user = authenticate(request, username=username, password=password)
    return user


def logout_view(request):
    logout(request)
    return redirect('main_page')
