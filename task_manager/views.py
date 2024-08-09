from django.shortcuts import render, redirect
from task_manager.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect


def index(request):
    return render(request, 'index.html')


@csrf_protect
def login_view(request):
    form_error = False

    if request.method == 'GET':
        clear_session_username(request)
        form = initialize_login_form_with_session(request)
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
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


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы разлогинены')
    return redirect('main_page')
