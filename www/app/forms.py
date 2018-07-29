"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from .models import Feedback


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'text', 'image')
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name', css_class='input-xlarge'),
        Field('large', css_class='input-xlarge'),
        Field('text', rows="3", css_class='input-xlarge'),
        Field('image'),
        FormActions(
            Submit('send_feedback', 'Отправить заявку', css_class="btn-primary"),
            Submit('close', 'Закрыть'),
        )
    )

