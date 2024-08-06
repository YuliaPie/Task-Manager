from django import forms
from .models import Task, Status, CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


NAME_EXISTS_ERROR = _("Задача с таким именем уже существует.")


class TaskForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[], required=True)  # Инициализируем пустой список
    executor = forms.ModelChoiceField(queryset=None, required=False, empty_label="---------")  # Инициализируем None

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = [("", "---------")] + [(status.id, status.name) for status in
                                                               Status.objects.all()]
        self.fields['executor'].queryset = CustomUser.objects.all()

        if self.instance and self.instance.pk:
            self.fields['status'].initial = self.instance.status.id
            if self.instance.executor:
                self.fields['executor'].initial = self.instance.executor.id
            else:
                pass
        self.fields['name'].label = 'Имя'
        self.fields['name'].widget.attrs.update({'placeholder': 'Имя'})
        self.fields['description'].label = 'Описание'
        self.fields['description'].widget.attrs.update(
            {'placeholder': 'Описание', 'required': False})
        self.fields['status'].label = 'Статус'
        self.fields['status'].widget.attrs.update({'placeholder': 'Статус'})
        self.fields['executor'].label = 'Исполнитель'
        self.fields['executor'].widget.attrs.update(
            {'placeholder': 'Исполнитель', 'required': False})

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['name', 'status']
        for field in required_fields:
            if cleaned_data.get(field) is None:
                self.add_error(field, 'Поле обязательно для заполнения.')
        return cleaned_data

    def clean_status(self):
        status_id = self.cleaned_data.get('status')
        if Status.objects.filter(id=status_id).exists():
            status = Status.objects.get(id=status_id)
            return status
        else:
            msg = 'Выберете объект в списке.'
            self.add_error('status', msg)
            return None

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.instance.pk is None:
            if Task.objects.filter(name=name).exists():
                raise ValidationError(NAME_EXISTS_ERROR)
        else:
            if Task.objects.exclude(
                    pk=self.instance.pk
            ).filter(name=name).exists():
                raise ValidationError(NAME_EXISTS_ERROR)
        return name


class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(required=False, label="Статус")
    executor = forms.ChoiceField(required=False, label="Исполнитель")
    show_my_tasks = forms.BooleanField(required=False, label="Показать только мои задачи")

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)

        # Инициализируем STATUS_CHOICES и EXECUTOR_CHOICES внутри метода __init__
        self.fields['status'].choices = [("", "---------")] + [(status.id, status.name) for status in
                                                               Status.objects.all()]
        self.fields['executor'].choices = [("", "---------")] + [(user.id, f"{user.name} {user.surname}") for user in
                                                                 CustomUser.objects.all()]
