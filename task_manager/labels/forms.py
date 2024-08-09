from django import forms
from .models import Label


class LabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(LabelForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['name'].widget.attrs.update({'placeholder': 'Имя'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Label.objects.filter(name=name).exists():
            raise forms.ValidationError(
                "Метка с таким именем уже существует.")
        return name
