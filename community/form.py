from django import forms
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget
from .models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div
from django.core.exceptions import ValidationError


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['section', 'name', 'description', 'pinned']
        widgets = {
            'description': SummernoteWidget(),
        }
        exclude = ['created_by', 'likes', 'dislikes']

    def clean(self):
        cleaned_data = super().clean()
        if not self.has_changed():
            raise ValidationError("You haven't made any changes to the post.")
        return cleaned_data

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
