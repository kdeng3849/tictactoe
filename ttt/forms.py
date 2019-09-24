from django import forms
from django.contrib.auth.models import User

class AddUserForm(forms.Form):
    username    = forms.CharField(widget=forms.TextInput(attrs={'id':'signupUsername'}))
    password    = forms.CharField(widget=forms.PasswordInput(attrs={'id':'signupPassword'}))
    email       = forms.CharField(widget=forms.TextInput(attrs={'id':'signupEmail'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class LoginForm(forms.Form):
    username    = forms.CharField(widget=forms.TextInput(attrs={'id':'loginUsername'}))
    password    = forms.CharField(widget=forms.PasswordInput(attrs={'id':'loginPassword'}))

    class Meta:
        model = User
        fields = ['username', 'password']