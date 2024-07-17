from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','password']
    def save(self):
        s=super().save(commit=False)
        s.password=make_password(self.cleaned_data['password'])
        s.save()
        return s

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())

class addressform(forms.Form):
    name=forms.CharField(max_length=50)
    phone_number=forms.IntegerField()
    pincode=forms.IntegerField()
    state=forms.CharField(max_length=50)
    city=forms.CharField(max_length=50)
    colony=forms.CharField(max_length=50)
    street=forms.CharField(max_length=50)


