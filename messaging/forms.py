from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]


class UserSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label="Search Users")
