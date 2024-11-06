from django import forms
from .models import Review


class RatingForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating"]
