from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Episode
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, Row, Column
from django_summernote.widgets import SummernoteWidget


class EpisodeForm(ModelForm):
    reason = forms.CharField(max_length=400, required=True,)

    class Meta:
        model = Episode
        fields = [
                'overall_episode_number',
                'season_episode_number',
                'season',
                'title',
                'plot',
                'synopsis',
                'air_date',
                'stardate',
                'image'
            ]
        widgets = {
            'plot': SummernoteWidget(),
        }
        exclude = ['approved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Create Episode'))
        self.helper.layout = Layout(
            Fieldset(
                'Episode Details',
                Div(
                    Div('overall_episode_number', css_class='col-md-3 mb-3'),
                    Div('season_episode_number', css_class='col-md-3 mb-3'),
                    Div('season', css_class='col-md-3 mb-3'),
                    Div('title', css_class='col-md-3 mb-3'),
                    css_class='row'
                ),
                Div(
                    Div('synopsis', css_class='col-md-6 mb-3'),
                    Div('plot', css_class='col-md-6 mb-3'),
                    css_class='row'
                ),
                Div(
                    Div('air_date', css_class='col-md-2 mb-3'),
                    Div('stardate', css_class='col-md-2 mb-3'),
                    Div('image', css_class='col-md-4 mb-3'),
                    Div('reason', css_class='col-md-4 mb-3'),
                    css_class='row'
                ),
            ),
        )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']
