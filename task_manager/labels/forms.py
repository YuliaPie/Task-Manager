from django import forms
from .models import Label


class BaseLabelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['name'].widget.attrs.update({'placeholder': 'Имя'})

    class Meta:
        abstract = True


class LabelForm(BaseLabelForm, forms.ModelForm):
    class Meta(BaseLabelForm.Meta):
        model = Label
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Label.objects.filter(name=name).exists():
            raise forms.ValidationError("Метка с таким именем уже существует.")
        return name
