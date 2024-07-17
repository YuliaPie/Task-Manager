from django import forms
from django.core.exceptions import ValidationError
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['surname'].label = 'Фамилия'
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].help_text = (
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и символы @/./+/-/_.'
        )
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Ваш пароль должен содержать как минимум 3 символа.'
        self.fields['password'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].help_text = 'Введите пароль еще раз для подтверждения.'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        if password and len(password) < 3:
            raise forms.ValidationError("Пароль должен содержать минимум 3 символа.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 150:
            raise ValidationError('Имя пользователя не должно превышать 150 символов.')
        if not username.replace('@', '').replace('.', '').replace('+', '').replace('-', '').replace('_', '').isalnum():
            raise ValidationError('Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_.')
        return username
