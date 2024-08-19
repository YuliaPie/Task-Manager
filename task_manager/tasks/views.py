from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy
from .forms import TaskFilterForm
import logging
from django.db.models import Q
from task_manager.tools import AuthRequiredMixin, AuthorPermissionMixin

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TaskListView(AuthRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        qs = super().get_queryset()
        filter_form = TaskFilterForm(self.request.GET or None)
        if filter_form.is_valid():
            status = filter_form.cleaned_data.get('status')
            executor = filter_form.cleaned_data.get('executor')
            label_id = filter_form.cleaned_data.get('label')
            self_tasks = filter_form.cleaned_data.get('self_tasks')

            query = Q()
            if status:
                query &= Q(status=status)
            if executor:
                query &= Q(executor=executor)
            if label_id:
                query &= Q(labels__in=[label_id])
            if self_tasks:
                query &= Q(author=self.request.user)

            return qs.filter(query).order_by('created_at')
        return qs.order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET or None)
        context['form_processed'] = context['filter_form'].is_valid()
        return context


class TaskCreateView(AuthRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = "Задача успешно создана"

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
    success_message = "Задача успешно изменена"


class TaskDeleteView(AuthRequiredMixin,
                     AuthorPermissionMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:tasks')
    template_name = 'tasks/task_confirm_delete.html'
    success_message = "Задача успешно удалена"
