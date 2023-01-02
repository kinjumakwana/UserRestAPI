from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth import get_user_model
from.models import *

class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email','mobile','address']
        labels = {'email': 'Email Address'}

class CustomAuthForm(AuthenticationForm):
        # email = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
        # password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
    def init(self, *args, **kwargs):
        super(CustomAuthForm, self).init(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class NotificationForm(forms.Form):
    Title = forms.CharField(label='Title', widget=forms.TextInput)
    Body = forms.CharField(label='Body', widget=forms.TextInput)
    
    # class Meta:
    #     model = Notification
    #     fields = ['Title', 'Body']
    #     labels = {'Title': 'Title'}
