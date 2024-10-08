from django import forms
from .models import Thread, Message, File

class CreateThread(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['name']

class CreateMessage(forms.ModelForm):
    thread_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Message
        fields = ['content', 'thread_id']

class CreateFile(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']