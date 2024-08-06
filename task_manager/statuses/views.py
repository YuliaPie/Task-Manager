from django.contrib.auth.views import redirect_to_login
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Status
from .forms import StatusForm
from django.contrib import messages
from django.urls import reverse


class IndexView(View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        return render(request, 'statuses/status_list.html', context={
            'statuses': statuses,
        })


class StatusFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = StatusForm()
        action_url = reverse('statuses:statuses_create')
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        return render(request,
                      'statuses/create.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        action_url = reverse('statuses:statuses_create')
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        if form.is_valid():
            new_status = form.save(commit=False)
            new_status.save()
            messages.success(request,
                             "Статус успешно добавлен",
                             extra_tags='success')
            return redirect('statuses:statuses')
        else:
            messages.error(request, None, extra_tags='danger')
            return render(request,
                          'statuses/create.html',
                          {'form': form, 'action_url': action_url})


class StatusFormEditView(View):
    def get(self, request, status_id):
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        status = get_object_or_404(Status, id=status_id)
        form = StatusForm(instance=status)
        action_url = reverse('statuses:statuses_update',
                             kwargs={'status_id': status.id})
        return render(request,
                      'statuses/update.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, status_id):
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path, '/login/', 'next')
        status = get_object_or_404(Status, id=status_id)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Статус успешно изменен",
                             extra_tags='success')
            return redirect('statuses:statuses')
        action_url = reverse('statuses:statuses_update',
                             kwargs={'status_id': status.id})
        messages.error(request, None, extra_tags='danger')
        return render(request,
                      'statuses/update.html',
                      {'form': form,
                       'action_url': action_url})


def status_confirm_delete(request, status_id):
    if not request.user.is_authenticated:
        messages.error(request,
                       "Вы не авторизованы! Пожалуйста, выполните вход.",
                       extra_tags='danger')
        return redirect_to_login(request.path, '/login/', 'next')
    status = get_object_or_404(Status, id=status_id)
    return render(request,
                  'statuses/status_confirm_delete.html',
                  {'status': status})


class StatusDeleteView(View):

    def post(self, request, status_id):
        status = Status.objects.get(id=status_id)
        if status:
            status.delete()
        messages.success(request, "Статус успешно удален.")
        return redirect('statuses:statuses')
