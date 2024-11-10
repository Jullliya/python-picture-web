from django import forms
from .models import Analyse


class ImageForm(forms.ModelForm):
    class Meta:
        model = Analyse
        fields = ('image', 'model_1', 'model_2', 'model_3', 'ensemble')
