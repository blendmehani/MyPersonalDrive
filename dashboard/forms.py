from django import forms
from .models import Requests
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ('full_name', 'email', 'message')

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        regex = r"[a-zA-Z0-9]+[\s][a-zA-Z0-9]+"
        validate = re.search(regex, full_name)
        if validate:
            return full_name
        raise forms.ValidationError('Please use your proper full name, e.g. "John Smith".')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
            return email
        except ValidationError:
            return False
