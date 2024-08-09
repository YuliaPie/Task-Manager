from django.shortcuts import redirect
from django.contrib import messages


def check_and_redirect_if_not_auth(request):
    if not request.user.is_authenticated:
        messages.error(
            request,
            "Вы не авторизованы! "
            "Пожалуйста, выполните вход.", extra_tags='danger')
        return redirect('login')
    return None
