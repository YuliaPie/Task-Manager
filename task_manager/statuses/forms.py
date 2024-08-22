from django import forms
from .models import Status
from django.utils.translation import gettext as _


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Name')
        self.fields['name'].widget.attrs.update({'placeholder': _('Name')})

    class Meta:
        abstract = True


class StatusForm(BaseModelForm):
    class Meta(BaseModelForm.Meta):
        model = Status
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Status.objects.filter(name=name).exists():
            raise forms.ValidationError(
                _("A status with this name already exists."))
        return name
