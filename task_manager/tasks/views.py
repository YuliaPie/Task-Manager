from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.urls import reverse
from .forms import TaskFilterForm
import logging
from django.db.models import Q
from task_manager.tools import check_and_redirect_if_not_auth


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        is_unauthorised = check_and_redirect_if_not_auth(request)
        if is_unauthorised:
            return is_unauthorised

        filter_form = TaskFilterForm(request.GET or None)
        tasks = Task.objects.all()
        author = request.user
        tasks = filter_tasks(tasks, filter_form, author)

        context = {
            'filter_form': filter_form,
            'tasks': tasks,
            'form_processed': filter_form.is_valid(),
        }
        return render(request, 'tasks/task_list.html', context)


def filter_tasks(tasks, filter_form, author):
    query = Q()
    if filter_form.is_valid():
        status = filter_form.cleaned_data.get('status')
        executor = filter_form.cleaned_data.get('executor')
        label_id = filter_form.cleaned_data.get('label')
        self_tasks = filter_form.cleaned_data.get('self_tasks')

        if status:
            query &= Q(status=status)
        if executor:
            query &= Q(executor=executor)
        if label_id:
            query &= Q(labels__in=[label_id])
        if self_tasks:
            query &= Q(author=author)

        return tasks.filter(query).order_by('created_at')
    return tasks.order_by('created_at')


class TaskFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        action_url = reverse('tasks:tasks_create')
        return (check_and_redirect_if_not_auth(request)
                or render(
                    request,
                    'tasks/create.html',
                    {'form': form,
                     'action_url': action_url}))

    def post(self, request, *args, **kwargs):
        action_url = reverse('tasks:tasks_create')
        is_unauthorised = check_and_redirect_if_not_auth(request)
        if is_unauthorised:
            return is_unauthorised
        form = TaskForm(request.POST)
        if form.is_valid():
            author = request.user
            labels = form.cleaned_data.get('labels')
            new_task = form.save(commit=False)
            new_task.author = author
            new_task.save()
            if labels:
                new_task.labels.set(labels)
            messages.success(request,
                             "Задача успешно создана",
                             extra_tags='success')
            return redirect('tasks:tasks')
        else:
            messages.error(request, None, extra_tags='danger')
            form_errors = form.errors
            return render(request,
                          'tasks/create.html',
                          {'form': form, 'form_errors': form_errors,
                           'action_url': action_url})


def task_info(request, task_id):
    return (check_and_redirect_if_not_auth(request)
            or render(request,
                      'tasks/info.html',
                      {'task': Task.objects.get(id=task_id)}))


class TaskFormEditView(View):
    def get(self, request, task_id):
        result = check_and_redirect_if_not_auth(request)
        if result:
            return result
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(instance=task)
        logger.debug(f"Form data: {form.as_p()}")
        action_url = reverse('tasks:task_update', kwargs={'task_id': task.id})
        return render(request,
                      'tasks/update.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, task_id):
        result = check_and_redirect_if_not_auth(request)
        if result:
            return result
        task = get_object_or_404(Task, id=task_id)
        author = task.author
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            labels = form.cleaned_data.get('labels')
            updated_task = form.save(commit=False)
            updated_task.author = author
            updated_task.save()
            if labels:
                updated_task.labels.set(labels)
            form.save()
            messages.success(request,
                             "Задача успешно изменена",
                             extra_tags='success')
            return redirect('tasks:tasks')
        action_url = reverse('tasks:task_update', kwargs={'task_id': task.id})
        messages.error(request, None, extra_tags='danger')
        return render(request,
                      'tasks/update.html',
                      {'form': form,
                       'action_url': action_url})


def task_confirm_delete(request, task_id):
    result = check_and_redirect_if_not_auth(request)
    if result:
        return result
    if not get_object_or_404(Task, id=task_id).author == request.user:
        messages.error(
            request,
            'Задачу может удалить только ее автор',
            extra_tags='danger')
        return redirect('tasks:tasks')
    render(request,
           'tasks/task_confirm_delete.html',
           {'task': get_object_or_404(Task, id=task_id)})


class TaskDeleteView(View):

    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        if task:
            task.delete()
        messages.success(request, "Задача успешно удалена.")
        return redirect('tasks:tasks')
