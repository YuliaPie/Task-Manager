from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class TaskManager(models.Manager):
    def create_task(self, **kwargs):
        task = self.model(**kwargs)
        if 'labels' in kwargs:
            task.labels.set(kwargs['labels'])
        task.save()
        return task


class Task(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='created_tasks'
                               )
    executor = models.ForeignKey(CustomUser,
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='executed_tasks'
                                 )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,
                               related_name='tasks', default=1)
    labels = models.ManyToManyField(Label,
                                    through='TaskLabel', related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TaskManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.author = kwargs.get('author') or self.author
        super().save(*args, **kwargs)
        self.labels.set(kwargs.get('labels', []))

    class Meta:
        ordering = ['-created_at']


class ProtectedByDependencyError(Exception):
    pass


@receiver(pre_delete, sender=CustomUser)
def prevent_user_deletion(sender, instance, **kwargs):
    if instance.created_tasks.exists() or instance.executed_tasks.exists():
        raise ProtectedByDependencyError(
            "Нельзя удалить пользователя, потому что он используется.")


class TaskLabel(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='task_labels')
    label = models.ForeignKey(Label,
                              on_delete=models.PROTECT,
                              related_name='task_labels')
