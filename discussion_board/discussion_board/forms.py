from django import forms
from django.core.exceptions import ValidationError


class CreatePostForm(forms.Form):
    title = forms.CharField(label='Post Title',
                            max_length=128,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    details = forms.CharField(label='Details',
                            max_length=8192,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    def check_title_details(self):
        title = self.cleaned_data['title']
        details = self.cleaned_data['details']
        if len(title) == 0 or len(details) == 0:
            raise ValidationError('Invalid - title or details should not be empty')
        else:
            return title, details

class CreateReplyForm(forms.Form):
    details = forms.CharField(label='Details',
                            max_length=1024,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    def check_details(self):
        details = self.cleaned_data['details']
        if len(details) == 0:
            raise ValidationError('Invalid - details should not be empty')
        else:
            return details





