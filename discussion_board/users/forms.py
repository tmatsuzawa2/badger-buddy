from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_registration.forms import RegistrationForm
from django import forms
from ..models import Profile

class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address.")
            
        return email


class UserRegistrationForm(RegistrationForm):    
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Overseer', 'Overseer')
    )
    user_type = forms.ChoiceField(label='User Type', widget=forms.Select(attrs={'class': 'form-control'}), choices=ROLE_CHOICES)
    anonymous = forms.BooleanField(label='Anonymity', widget=forms.CheckboxInput(attrs={'class': 'form-check'}), required=False)

    class Meta(RegistrationForm.Meta):
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            'first_name',
            'last_name',
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        print(self.fields["anonymous"].required)

        email_field = User.get_email_field_name()
        self.fields[email_field].validators.append(
            RegexValidator(r'^([\w-]+(?:\.[\w-]+)*)@wisc.edu|^([\w-]+(?:\.[\w-]+)*)@((?:[\w-].)*\w[\w-]{0,5})\.wisc.edu', message="Please enter a wisc email")
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        user.profile.user_type = self.cleaned_data['user_type']
        user.profile.anonymous = self.cleaned_data['anonymous']
        if commit:
            user.save()
        return user