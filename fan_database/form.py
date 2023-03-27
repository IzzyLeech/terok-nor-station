from django.forms import ModelForm
from django import forms
from .models import Episode


class EpisodeForm(ModelForm):
    class Meta:
        model = Episode
        fields = '__all__'


