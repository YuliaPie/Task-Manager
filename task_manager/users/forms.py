from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


USERNAME_EXISTS_ERROR = _("Пользователь с таким именем уже существует.")
PASSWORD_MISMATCH_ERROR = _("Введенные пароли не совпадают.")
MINIMUM_PASSWORD_LENGTH_ERROR = _("Введённый пароль "
                                  "слишком короткий. "
                                  "Он должен содержать как "
                                  "минимум 3 символа.")


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            render_value=True
        ), required=True, initial='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            render_value=True
        ), required=True, initial='')

    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'username', 'password', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['name'].widget.attrs.update({'placeholder': 'Имя'})

        self.fields['surname'].label = 'Фамилия'
        self.fields['surname'].widget.attrs.update({'placeholder': 'Фамилия'})

        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].help_text = (
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и символы @/./+/-/_.'
        )
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Имя пользователя'})

        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text =\
            'Ваш пароль должен содержать как минимум 3 символа.'
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})

        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].help_text =\
            'Для подтверждения введите, пожалуйста, пароль ещё раз.'
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Подтверждение пароля'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.pk is None:
            if CustomUser.objects.filter(username=username).exists():
                raise ValidationError(USERNAME_EXISTS_ERROR)
        else:
            if CustomUser.objects.exclude(
                    pk=self.instance.pk
            ).filter(username=username).exists():
                raise ValidationError(USERNAME_EXISTS_ERROR)

        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': PASSWORD_MISMATCH_ERROR,
            })
        if password and len(password) < 3:
            raise ValidationError({
                'password2': MINIMUM_PASSWORD_LENGTH_ERROR,
            })
        return cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
