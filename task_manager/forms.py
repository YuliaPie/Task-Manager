from django import forms
from task_manager.users.models import CustomUser
from django.utils.translation import gettext as _


class LoginForm(forms.Form):
    username = forms.CharField(label=_('User name'), max_length=150)
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = CustomUser.objects.filter(username=username).first()

        if not user:
            raise forms.ValidationError(_("User not found"))

        if not user.check_password(password):
            raise forms.ValidationError(_("Wrong password"))

        return cleaned_data
