from django import forms
from .models import Task, Status, CustomUser


class TaskForm(forms.ModelForm):
    status = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label="---------")
    executor = forms.ModelChoiceField(queryset=CustomUser.objects.all(), empty_label="---------")
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['name'].widget.attrs.update({'placeholder': 'Имя'})
        self.fields['description'].label = 'Описание'
        self.fields['description'].widget.attrs.update({'placeholder': 'Описание'})
        self.fields['status'].label = 'Статус'
        self.fields['status'].widget.attrs.update({'placeholder': 'Статус'})
        self.fields['executor'].label = 'Исполнитель'
        self.fields['executor'].widget.attrs.update({'placeholder': 'Исполнитель'})


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [("", "---------")] + [(status.id, status.name) for status in Status.objects.all()]
    EXECUTOR_CHOICES = [("", "---------")] + [(user.id, f"{user.name} {user.surname}") for user in CustomUser.objects.all()]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Статус")
    executor = forms.ChoiceField(choices=EXECUTOR_CHOICES, label="Исполнитель")
    show_my_tasks = forms.BooleanField(required=False, label="Показать только мои задачи")
