from django import forms
from .models import Tweet , Profile
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django.contrib.auth.models import User 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']

    def __init__(self, *args, **kwargs):
        super(TweetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('text', css_class="block w-full p-3 border rounded-md bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors"),
            Field('photo', css_class="block w-full p-3 border rounded-md bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors"),
        )

        # Apply Dark Mode classes to all input fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'block w-full p-3 border rounded-md bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors focus:ring-blue-500 focus:border-blue-500',
            })

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Corrected typo

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'block w-full p-3 border rounded-md bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors'}),
            'email': forms.EmailInput(attrs={'class': 'block w-full p-3 border rounded-md bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'block w-full p-3 border rounded-md bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors'}),
            'profile_picture': forms.FileInput(attrs={'class': 'block w-full p-3 border rounded-md bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors'}),
        }
