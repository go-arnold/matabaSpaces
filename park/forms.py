from django import forms
from .models import LostRequest



class LostRequestResponseForm(forms.ModelForm):
    class Meta:
        model = LostRequest
        fields = ['response']