from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=32)

    def check_title_details(self):
        title = self.cleaned_data['title']
        details = self.cleaned_data['details']
        if len(title) == 0 or len(details) == 0:
            raise ValidationError('Invalid - title or details should not be empty')
        else:
            return title, details


