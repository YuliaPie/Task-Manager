from django.contrib.auth.views import redirect_to_login
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.urls import reverse
from .forms import TaskFilterForm
import logging
from django.db.models import Q


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class IndexView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')

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
            show_my_tasks = filter_form.cleaned_data.get('show_my_tasks')
            query = Q()
            if status:
                query &= Q(status=status)
            if executor:
                query &= Q(executor=executor)
            if show_my_tasks:
                query &= Q(author=request.user)
            tasks = tasks.filter(query).order_by('created_at')

            context = {
                'filter_form': filter_form,
                'tasks': tasks,
                'form_processed': True,  # Форма была обработана
            }

        return render(request, 'tasks/task_list.html', context)


class TaskFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        action_url = reverse('tasks:tasks_create')
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        return render(request,
                      'tasks/create.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, *args, **kwargs):
        action_url = reverse('tasks:tasks_create')
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        logger.debug(request)
        form = TaskForm(request.POST)
        logger.debug(form)
        if form.is_valid():
            author = request.user
            new_task = form.save(commit=False)
            new_task.author = author
            new_task.save()
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
    if not request.user.is_authenticated:
        messages.error(request,
                       "Вы не авторизованы! Пожалуйста, выполните вход.",
                       extra_tags='danger')
        return redirect_to_login(request.path,
                                 '/login/',
                                 'next')
    task = Task.objects.get(id=task_id)
    return render(request,
                  'tasks/info.html',
                  {'task': task})


class TaskFormEditView(View):
    def get(self, request, task_id):
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(instance=task)
        logger.debug(f"Form data: {form.as_p()}")
        action_url = reverse('tasks:task_update', kwargs={'task_id': task.id})
        return render(request,
                      'tasks/update.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, task_id):
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path, '/login/', 'next')
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
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
    if not request.user.is_authenticated:
        messages.error(request,
                       "Вы не авторизованы! Пожалуйста, выполните вход.",
                       extra_tags='danger')
        return redirect_to_login(request.path, '/login/', 'next')
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


class TaskDeleteView(View):

    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        if task:
            task.delete()
        messages.success(request, "Задача успешно удалена.")
        return redirect('tasks:tasks')
