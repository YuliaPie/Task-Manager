from django.db import models
from django.utils.translation import gettext as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser


class Task(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.PROTECT,
                               related_name='created_tasks',
                               verbose_name=_('Author'),
                               )
    executor = models.ForeignKey(CustomUser,
                                 null=True,
                                 blank=True,
                                 on_delete=models.PROTECT,
                                 related_name='executed_tasks',
                                 verbose_name=_('Executor'),
                                 )
    name = models.CharField(max_length=255,
                            verbose_name=_('Name'), )
    description = models.TextField(blank=True,
                                   verbose_name=_('Description'), )
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               related_name='tasks',
                               verbose_name=_('Status'), )
    labels = models.ManyToManyField(Label,
                                    through='TaskLabel',
                                    related_name='tasks',
                                    blank=True,
                                    verbose_name=_('Labels'), )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='task_labels')
    label = models.ForeignKey(Label,
                              on_delete=models.PROTECT,
                              related_name='task_labels')
