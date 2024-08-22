from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView
                                  )
from .forms import TaskForm
from django.urls import reverse_lazy
import logging
from task_manager.tools import AuthRequiredMixin, AuthorPermissionMixin
from django_filters.views import FilterView
from .models import Task
from .filters import TaskFilter
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TaskListView(AuthRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(AuthRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _("Task created successfully")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(AuthRequiredMixin,
                     DetailView):
    model = Task
    template_name = 'tasks/info.html'


class TaskEditView(AuthRequiredMixin,
                   SuccessMessageMixin,
                   UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _("Task modified successfully")


class TaskDeleteView(SuccessMessageMixin,
                     AuthRequiredMixin,
                     AuthorPermissionMixin,
                     UserPassesTestMixin,
                     DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:tasks')
    template_name = 'tasks/task_confirm_delete.html'
    success_message = _("Task successfully deleted")
