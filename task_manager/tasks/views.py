from django.contrib.auth.views import redirect_to_login
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.urls import reverse
from .forms import TaskFilterForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')

        filter_form = TaskFilterForm(request.GET)
        tasks = Task.objects.all()

        if filter_form.is_valid():
            status = filter_form.cleaned_data.get('status')
            executor = filter_form.cleaned_data.get('executor')
            show_my_tasks = filter_form.cleaned_data.get('show_my_tasks')

            if status:
                tasks = tasks.filter(status=status)
            elif executor:
                tasks = tasks.filter(executor=executor)
            if show_my_tasks:
                tasks = tasks.filter(author=request.user)
        return render(request, 'tasks/task_list.html', {'filter_form': filter_form, 'tasks': tasks})


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
        form = TaskForm(request.POST)
        action_url = reverse('tasks:tasks_create')
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.save()
            messages.success(request,
                             "Задача успешно добавлена",
                             extra_tags='success')
            return redirect('tasks:tasks')
        else:
            messages.error(request, None, extra_tags='danger')
            return render(request,
                          'tasks/create.html',
                          {'form': form, 'action_url': action_url})


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
        action_url = reverse('tasks:tasks_update', kwargs={'task_id': task.id})
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
        action_url = reverse('tasks:tasks_update', kwargs={'task_id': task.id})
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
