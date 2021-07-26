from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML, Div
from profiles.models import Profile


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput)
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'gender',
        )

    class Media:
        js = ('common/js/gijgo.min.js',)
        css = {
            'all': ('common/css/gijgo.min.css',)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('last_name', wrapper_class='col-sm-12 col-md-4 mb-3'),
                Field('first_name', wrapper_class='col-sm-12 col-md-4 mb-3'),
                Field('middle_name', wrapper_class='col-sm-12 col-md-4 mb-3'),
                css_class='row'
            ),
            Div(
                Field('date_of_birth', wrapper_class='col-sm-12 col-md-6 mb-3', placeholder='YYYY-MM-DD (ex: 1990-12-31)'),
                Field('gender', wrapper_class='col-sm-12 col-md-6 mb-3'),
                css_class='row'
            )
        )