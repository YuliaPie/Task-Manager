from urllib import request

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib import messages

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser


@receiver(pre_delete, sender=CustomUser)
def prevent_user_deletion(sender, instance, **kwargs):
    if instance.created_tasks.exists() or instance.executed_tasks.exists():
        messages.error(
            request,
            'Невозможно удалить пользователя, '
            'потому что он используется.',
            extra_tags='danger')
        return False


@receiver(pre_delete, sender=Status)
def prevent_status_deletion(sender, instance, **kwargs):
    if Task.objects.filter(status=instance).exists():
        messages.error(request,
                       "Невозможно удалить статус, "
                       "потому что он используется",
                       extra_tags='danger')
        return False


@receiver(pre_delete, sender=Label)
def prevent_label_deletion(sender, instance, **kwargs):
    if Task.objects.filter(task_labels__label=instance).exists():
        messages.error(
            request,
            'Невозможно удалить метку, потому что она используется',
            extra_tags='danger')
        return False
