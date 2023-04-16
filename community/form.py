from django import forms
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget
from .models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['section', 'name', 'description', 'pinned']
        widgets = {
            'description': SummernoteWidget(),
        }
        exclude = ['created_by', 'likes', 'dislikes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not user or not user.is_superuser:
            self.fields['pinned'].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Create Post'))
        self.helper.layout = Layout(
            Fieldset(
                'Post details',
                Div(
                    Div('section', css_class='col-md-6'),
                    Div('name', css_class='col-md-6'),
                    css_class='row'
                ),
                Div(
                    Div('description', css_class='col-md-12'),
                    css_class='row'
                ),
                'pinned'
            )
        )
