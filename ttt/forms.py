from django import forms

class AddUserForm(forms.Form):
    username    = forms.CharField()
    password    = forms.CharField()
    email       = forms.CharField()