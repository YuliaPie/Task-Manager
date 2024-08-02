from django import forms
from .models import Task, Status, CustomUser


class TaskForm(forms.ModelForm):
    STATUS_CHOICES = [("", "---------")] + [(status.id, status.name) for status in Status.objects.all()]

    # Используем empty_label для ChoiceField
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True)

    # Создаем начальный список с пустым значением для executor
    EXECUTOR_CHOICES = [("", "---------")] + [(user.id, f"{user.name} {user.surname}") for user in
                                              CustomUser.objects.all()]

    # Используем empty_label для ModelChoiceField
    executor = forms.ModelChoiceField(queryset=CustomUser.objects.all(),
                                      required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['name'].widget.attrs.update({'placeholder': 'Имя'})
        self.fields['description'].label = 'Описание'
        self.fields['description'].widget.attrs.update({'placeholder': 'Описание', 'required': False})
        self.fields['status'].label = 'Статус'
        self.fields['status'].widget.attrs.update({'placeholder': 'Статус'})
        self.fields['executor'].label = 'Исполнитель'
        self.fields['executor'].widget.attrs.update({'placeholder': 'Исполнитель', 'required': False})

    def clean_status(self):
        status_id = self.cleaned_data.get('status')
        if Status.objects.filter(id=status_id).exists():
            status = Status.objects.get(id=status_id)
            return status
        else:
            msg = 'Неверный статус.'
            self.add_error('status', msg)
            return None


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [("", "---------")] + [(status.id, status.name) for status in Status.objects.all()]
    EXECUTOR_CHOICES = [("", "---------")] + [(user.id, f"{user.name} {user.surname}") for user in CustomUser.objects.all()]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Статус")
    executor = forms.ChoiceField(choices=EXECUTOR_CHOICES, label="Исполнитель")
    show_my_tasks = forms.BooleanField(required=False, label="Показать только мои задачи")
