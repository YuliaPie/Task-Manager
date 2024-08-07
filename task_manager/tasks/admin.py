from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('author', 'executor', 'name', 'description', 'status', 'labels_str')
    search_fields = ['author', 'executor', 'name', 'description', 'status', 'labels']

    def labels_str(self, obj):
        return ', '.join([label.name for label in obj.labels.all()])

    labels_str.short_description = 'Метки'
    list_filter = (('created_at', DateFieldListFilter),)
