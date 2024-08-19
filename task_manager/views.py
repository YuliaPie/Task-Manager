from django.shortcuts import render, redirect
from django.views import View
from task_manager.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from task_manager.tools import (clear_session_username,
                                initialize_login_form_with_session)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        clear_session_username(request)
        form = initialize_login_form_with_session(request)
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы залогинены')
                return redirect('main_page')
            else:
                form_error = True
                request.session['username'] = username
                request.session.modified = True
        else:
            form_error = True

        if 'username' in request.POST:
            request.session['username'] = request.POST['username']
            request.session.modified = True

        return render(request, 'login.html',
                      {'form': form,
                       'form_error': form_error})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'Вы разлогинены')
        return redirect('main_page')
