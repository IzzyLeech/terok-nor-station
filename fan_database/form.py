from django.forms import ModelForm
from .models import Episode


class EpisodeForm(ModelForm):
    class Meta:
        model = Episode
        fields = '__all__'
