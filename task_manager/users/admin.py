from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'username')
    search_fields = ['name', 'surname', 'username']
    list_filter = (('created_at', DateFieldListFilter),)
