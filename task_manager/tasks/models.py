from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser


class Task(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.PROTECT,
                               related_name='created_tasks'
                               )
    executor = models.ForeignKey(CustomUser,
                                 null=True,
                                 blank=True,
                                 on_delete=models.PROTECT,
                                 related_name='executed_tasks'
                                 )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               related_name='tasks', default=1)
    labels = models.ManyToManyField(Label,
                                    through='TaskLabel', related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.author = kwargs.get('author') or self.author
        super().save(*args, **kwargs)
        self.labels.set(kwargs.get('labels', []))

    class Meta:
        ordering = ['-created_at']


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='task_labels')
    label = models.ForeignKey(Label,
                              on_delete=models.PROTECT,
                              related_name='task_labels')
