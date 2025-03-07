from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        filds = ['text', 'photo']
        exclude = ['user']  # Exclude specific fields if needed
