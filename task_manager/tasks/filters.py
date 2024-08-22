from django_filters import BooleanFilter, ModelChoiceFilter, FilterSet
from .models import Task
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Status, CustomUser, Label


class TaskFilter(FilterSet):
    self_tasks = BooleanFilter(
        label=_('Show only my tasks'),
        method='filter_self_tasks',
        widget=forms.CheckboxInput,
    )

    status = ModelChoiceFilter(label=_('Status'), queryset=Status.objects.all())
    executor = ModelChoiceFilter(label=_('Executor'), queryset=CustomUser.objects.all())
    labels = ModelChoiceFilter(label=_('Labels'), queryset=Label.objects.all())

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset
