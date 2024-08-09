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
        result = check_and_redirect_if_not_auth(request)
        if result:
            return result
        filter_form = TaskFilterForm(request.GET or None)

        tasks = Task.objects.all().order_by('created_at')
        context = {
            'filter_form': filter_form,
            'tasks': tasks,
            'form_processed': False,
        }
        if filter_form.is_valid():
            status = filter_form.cleaned_data.get('status')
            executor = filter_form.cleaned_data.get('executor')
            label_id = filter_form.cleaned_data.get('label')
            show_my_tasks = filter_form.cleaned_data.get('show_my_tasks')
            query = Q()
            if status:
                query &= Q(status=status)
            if executor:
                query &= Q(executor=executor)
            if label_id:
                query &= Q(labels__in=[label_id])
            if show_my_tasks:
                query &= Q(author=request.user)
            tasks = tasks.filter(query).order_by('created_at')

            context = {
                'filter_form': filter_form,
                'tasks': tasks,
                'form_processed': True,
            }

        return render(request, 'tasks/task_list.html', context)


class TaskFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        action_url = reverse('tasks:tasks_create')
        result = check_and_redirect_if_not_auth(request)
        if result:
            return result
        return render(request,
                      'tasks/create.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, *args, **kwargs):
        action_url = reverse('tasks:tasks_create')
        result = check_and_redirect_if_not_auth(request)
        if result:
            return result
        logger.debug(request)
        form = TaskForm(request.POST)
        logger.debug(form)
        if form.is_valid():
            author = request.user
            labels = form.cleaned_data.get('labels')
            new_task = form.save(commit=False)
            new_task.author = author
            new_task.save()
            if labels:
                new_task.labels.set(labels)
            messages.success(request,
                             "Задача успешно добавлена",
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
    result = check_and_redirect_if_not_auth(request)
    if result:
        return result
    task = Task.objects.get(id=task_id)
    return render(request,
                  'tasks/info.html',
                  {'task': task})


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
                             "Задача успешно измененa",
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
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


class TaskDeleteView(View):

    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        if task:
            task.delete()
        messages.success(request, "Задача успешно удалена.")
        return redirect('tasks:tasks')
