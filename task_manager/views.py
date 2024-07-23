from django.shortcuts import render, redirect
from task_manager.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect


def index(request):
    return render(request, 'index.html')


@csrf_protect
def login_view(request):
    if request.method == 'GET':
        try:
            del request.session['username']
        except KeyError:
            pass

    if request.method == 'POST':
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
                messages.error(request,
                               'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
                request.session['username'] = username
                request.session.modified = True
        else:
            if 'username' in request.POST:
                request.session['username'] = request.POST['username']
                request.session.modified = True
            messages.error(request, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')

    else:
        form = LoginForm()

    if 'username' in request.session:
        form.fields['username'].initial = request.session.get('username', '')
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы разлогинены')
    return redirect('main_page')
