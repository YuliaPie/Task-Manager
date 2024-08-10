from django.db.models import ProtectedError
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Label
from .forms import LabelForm
from django.contrib import messages
from django.urls import reverse
from task_manager.tools import check_and_redirect_if_not_auth


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return (check_and_redirect_if_not_auth(request)
                or render(request,
                          'labels/label_list.html',
                          context={'labels': Label.objects.all()}))


class LabelFormCreateView(View):
    def get(self, request, *args, **kwargs):
        return (check_and_redirect_if_not_auth(request)
                or render(
                    request,
                    'labels/create.html',
                    {'form': LabelForm(), 'action_url': reverse('labels:labels_create')}))

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        action_url = reverse('labels:labels_create')
        result = check_and_redirect_if_not_auth(request)
        if result:
            return result
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
        return (check_and_redirect_if_not_auth(request)
                or render(
                    request,
                    'labels/update.html',
                    {
                        'form':
                            LabelForm(
                                instance=get_object_or_404(
                                    Label,
                                    id=label_id)),
                        'action_url': reverse(
                            'labels:labels_update',
                            kwargs={'label_id': label_id})}))

    def post(self, request, label_id):
        is_unauthorised = check_and_redirect_if_not_auth(request)
        if is_unauthorised:
            return is_unauthorised
        else:
            form = LabelForm(
                request.POST,
                instance=get_object_or_404(
                    Label,
                    id=label_id))
            if form.is_valid():
                form.save()
                messages.success(request,
                                 "Метка успешно изменена",
                                 extra_tags='success')
                return redirect('labels:labels')
            action_url = reverse('labels:labels_update',
                                 kwargs={'label_id': label_id})
            messages.error(request, None,
                           extra_tags='danger')
            return render(
                request,
                'labels/update.html',
                {'form': form, 'action_url': action_url})


def label_confirm_delete(request, label_id):
    return (check_and_redirect_if_not_auth(request)
            or render(
                request,
                'labels/label_confirm_delete.html',
                {'label': get_object_or_404(
                    Label,
                    id=label_id)}))


class LabelDeleteView(View):

    def post(self, request, label_id):
        label = Label.objects.get(id=label_id)
        if label:
            try:
                label.delete()
            except ProtectedError:
                messages.error(
                    request,
                    'Невозможно удалить метку, потому что она используется.',
                    extra_tags='danger')
                return redirect('labels:labels')
        messages.success(request, "Метка успешно удалена.")
        return redirect('labels:labels')
