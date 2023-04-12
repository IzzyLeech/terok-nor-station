from django import forms
from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['created_by', 'likes', 'dislikes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not user or not user.is_superuser:
            self.fields['pinned'].widget = forms.HiddenInput()
