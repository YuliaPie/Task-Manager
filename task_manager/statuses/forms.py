from django import forms
from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['name'].widget.attrs.update({'placeholder': 'Имя'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Status.objects.filter(name=name).exists():
            raise forms.ValidationError(
                "Статус с таким именем уже существует.")
        return name
