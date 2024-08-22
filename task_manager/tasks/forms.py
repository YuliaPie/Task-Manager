from django import forms
from .models import Task, Status, CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import logging
from task_manager.labels.models import Label

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

NAME_EXISTS_ERROR = _("A task with this name already exists.")


class TaskForm(forms.ModelForm):
    status =\
        forms.ChoiceField(
            choices=[],
            required=True)
    executor =\
        forms.ModelChoiceField(
            queryset=None,
            required=False,
            empty_label="---------")
    labels =\
        forms.ModelMultipleChoiceField(
            queryset=Label.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices \
            = ([("", "---------")]
               + [(status.id, status.name)
                  for status in
                  Status.objects.all()])
        self.fields['executor'].queryset = CustomUser.objects.all()
        self.fields['executor'].choices \
            = ([("", "---------")]
               + [(user.id,
                   f"{user.first_name} {user.last_name}") for user in
                  CustomUser.objects.all()])
        self.fields['executor'].initial = ""

        if self.instance and self.instance.pk:
            self.fields['status'].initial = self.instance.status.id
            if self.instance.executor:
                self.fields['executor'].initial = self.instance.executor.id
            else:
                pass
        self.fields['name'].label = _("Name")
        self.fields['name'].widget.attrs.update({'placeholder': _("Name")})
        self.fields['description'].label = _('Description')
        self.fields['description'].widget.attrs.update(
            {'placeholder': _('Description'), 'required': False})
        self.fields['status'].label = _('Status')
        self.fields['status'].widget.attrs.update({'placeholder': _('Status')})
        self.fields['executor'].label = _('Executor')
        self.fields['executor'].widget.attrs.update(
            {'placeholder': _('Executor'), 'required': False})
        self.fields['labels'].label = _('Labels')
        self.fields['labels'].widget.attrs.update(
            {'placeholder': _('Labels'), 'required': False})

    def clean(self):
        cleaned_data = super().clean()
        logger.info(f"Cleaned data: {cleaned_data}")
        required_fields = ['name', 'status']
        for field in required_fields:
            if cleaned_data.get(field) is None:
                self.add_error(field, _('This field is required.'))
        return cleaned_data

    def clean_status(self):
        status_pk = self.cleaned_data.get('status')
        if Status.objects.filter(pk=status_pk).exists():
            status = Status.objects.get(pk=status_pk)
            return status
        else:
            msg = _('Select an object from the list.')
            self.add_error('status', msg)
            return None

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.instance.pk is None:
            if Task.objects.filter(name=name).exists():
                raise ValidationError(NAME_EXISTS_ERROR)
            return name
        if Task.objects.exclude(
                pk=self.instance.pk).filter(name=name).exists():
            raise ValidationError(NAME_EXISTS_ERROR)
        return name
