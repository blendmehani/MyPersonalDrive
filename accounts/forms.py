from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'email', 'country', 'city', 'phone_number',
                  'birthdate', 'secret_question', 'secret_answer', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Wrong credentials. Check your email address and your password.')
