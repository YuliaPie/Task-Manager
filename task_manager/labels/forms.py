from django import forms
from .models import Label
from django.utils.translation import gettext as _


class LabelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Name')
        self.fields['name'].widget.attrs.update({'placeholder': _('Name')})

    class Meta():
        model = Label
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Label.objects.filter(name=name).exists():
            raise forms.ValidationError(_(
                "A label with this name already exists."))
        return name
