from django import forms
from .models import Thread, Message

class CreateThread(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['name']

class CreateMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['type','content', 'thread']