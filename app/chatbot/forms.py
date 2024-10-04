from django import forms
from .models import Thread

class CreateThread(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['name']