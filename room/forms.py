from django.forms import ModelForm
from .models import Room
from django import forms

class CreateRoom(ModelForm):
    class Meta:
        model = Room
        fields = ('name','password',)