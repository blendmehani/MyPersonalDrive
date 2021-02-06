from django import forms
from accounts.models import User
from .models import File


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        email = str(email)
        raise forms.ValidationError(f"Email Address {email} is already in use. ")


class UploadFile(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)

