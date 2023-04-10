from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Episode


class EpisodeForm(ModelForm):
    reason = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Episode
        fields = '__all__'
        exclude = ['approved']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
