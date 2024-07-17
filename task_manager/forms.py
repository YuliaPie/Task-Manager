from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from task_manager.users.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
            if not check_password(password, user.password):  # Используйте check_password вместо user.check_password
                raise ValidationError('Неверный логин или пароль.')
        except User.DoesNotExist:
            raise ValidationError('Пользователь не найден.')
        return cleaned_data
