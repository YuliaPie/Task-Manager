from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from task_manager.users.models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username or not password:
            raise forms.ValidationError('Оба поля должны быть заполнены.')

        user = CustomUser.objects.filter(username=username).first()
        if not user:
            raise ValidationError('Пользователь не найден.')

        if not check_password(password, user.password):
            raise ValidationError('Неверный логин или пароль.')
        return cleaned_data
