from django import forms
from .models import Status


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['name'].widget.attrs.update({'placeholder': 'Имя'})

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
                "Статус с таким именем уже существует.")
        return name
