from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    name = forms.CharField(label='Jméno', max_length=30)
    password = forms.CharField(label='Heslo', widget=forms.PasswordInput)
