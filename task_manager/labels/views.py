from django.contrib.auth.views import redirect_to_login
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Label
from .forms import LabelForm
from django.contrib import messages
from django.urls import reverse
from django.db.models import ProtectedError


class IndexView(View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        return render(request, 'labels/label_list.html', context={
            'labels': labels,
        })


class LabelFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = LabelForm()
        action_url = reverse('labels:labels_create')
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        return render(request,
                      'labels/create.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        action_url = reverse('labels:labels_create')
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        if form.is_valid():
            new_label = form.save(commit=False)
            new_label.save()
            messages.success(request,
                             "Метка успешно добавлена",
                             extra_tags='success')
            return redirect('labels:labels')
        else:
            messages.error(request, None, extra_tags='danger')
            return render(request,
                          'labels/create.html',
                          {'form': form, 'action_url': action_url})


class LabelFormEditView(View):
    def get(self, request, label_id):
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path,
                                     '/login/',
                                     'next')
        label = get_object_or_404(Label, id=label_id)
        form = LabelForm(instance=label)
        action_url = reverse('labels:labels_update',
                             kwargs={'label_id': label.id})
        return render(request,
                      'labels/update.html',
                      {'form': form, 'action_url': action_url})

    def post(self, request, label_id):
        if not request.user.is_authenticated:
            messages.error(request,
                           "Вы не авторизованы! Пожалуйста, выполните вход.",
                           extra_tags='danger')
            return redirect_to_login(request.path, '/login/', 'next')
        label = get_object_or_404(Label, id=label_id)
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Метка успешно изменена",
                             extra_tags='success')
            return redirect('labels:labels')
        action_url = reverse('labels:labels_update',
                             kwargs={'label_id': label.id})
        messages.error(request, None, extra_tags='danger')
        return render(request,
                      'labels/update.html',
                      {'form': form,
                       'action_url': action_url})


def label_confirm_delete(request, label_id):
    if not request.user.is_authenticated:
        messages.error(request,
                       "Вы не авторизованы! Пожалуйста, выполните вход.",
                       extra_tags='danger')
        return redirect_to_login(request.path, '/login/', 'next')
    label = get_object_or_404(Label, id=label_id)
    return render(request,
                  'labels/label_confirm_delete.html',
                  {'label': label})


class LabelDeleteView(View):

    def post(self, request, label_id):
        label = Label.objects.get(id=label_id)
        if label:
            try:
                label.delete()
            except ProtectedError:
                messages.error(request, 'Невозможно удалить метку, потому что она используется.',
                               extra_tags='danger')
                return redirect('labels:labels')
        messages.success(request, "Метка успешно удалена.")
        return redirect('labels:labels')
