from django import forms
from .models import Letter


class LetterForm(forms.ModelForm):
    message = forms.CharField(label='', min_length=40, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Letter
        fields = ('message',)
