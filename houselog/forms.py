from django.forms import ModelForm
from houselog.models import Houselog
from django import forms
from django.contrib.auth.models import User

class AddItemForm(ModelForm):
    class Meta:
        model = Houselog
        fields = ['title', 'frequency', 'last_done', 'user']
        
class EditItemForm(ModelForm):
    class Meta:
        model = Houselog
        fields = ['id', 'title', 'frequency', 'last_done']
        widgets = {
            'id': forms.HiddenInput(),
        }