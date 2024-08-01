from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('author', 'executor', 'name', 'description', 'status',)
    search_fields = ['author', 'executor', 'name', 'description', 'status']
    list_filter = (('created_at', DateFieldListFilter),)
