from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

USERNAME_EXISTS_ERROR = _("A user with that name already exists.")
PASSWORD_MISMATCH_ERROR = _("The passwords entered do not match.")
MINIMUM_PASSWORD_LENGTH_ERROR = _("The password you entered is too short. "
                                  "It must contain at least 3 characters.")


class UserForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            render_value=True
        ), required=True, initial='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            render_value=True
        ), required=True, initial='')

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = _('Name')
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': _('Name')}, required=True)

        self.fields['last_name'].label = _('Surname')
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': _('Surname')},
            required=True)

        self.fields['username'].label = _('User name')
        self.fields['username'].help_text = _(
            'Required field. No more than 150 characters. '
            'Only letters, numbers and symbols @/./+/-/_.'
        )
        self.fields['username'].widget.attrs.update(
            {'placeholder': _('User name')})

        self.fields['password1'].label = _('Password')
        self.fields['password1'].help_text = _(
            'Your password must be at least 3 characters long.')
        self.fields['password1'].widget.attrs.update(
            {'placeholder': _('Password')})
        self.fields['password2'].label = _('Confirm password')
        self.fields['password2'].help_text = _(
            'Please enter your password again to confirm.')
        self.fields['password2'].widget.attrs.update(
            {'placeholder': _('Confirm password')})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.pk is None:
            if CustomUser.objects.filter(username=username).exists():
                raise ValidationError(USERNAME_EXISTS_ERROR)
        else:
            if CustomUser.objects.exclude(
                    pk=self.instance.pk).filter(username=username).exists():
                raise ValidationError(USERNAME_EXISTS_ERROR)
        return username


class UserUpdateForm(UserForm):
    password1 = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'password'}),
        required=True)
    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'password'}),
        required=True)

    class Meta(UserForm.Meta):
        fields = UserForm.Meta.fields + ['password1', 'password2']
