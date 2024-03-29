from django import forms
from django.db import models
from django.forms import Form, fields, widgets
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation

from app.models import Customer

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    password2 = forms.CharField(label='Confirm Password',
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    email = forms.CharField(required=True,
    widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))
    
    password  = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}))


class ChangePwdForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, 
    widget=forms.PasswordInput(attrs=
    {'class': 'form-control', 'autofocus': True, 'autocomplete': 'current-password'}))
    
    new_password1 = forms.CharField(label=_("New Password"), strip=False, 
    widget=forms.PasswordInput(attrs=
    {'class': 'form-control', 'help_text': password_validation.password_validators_help_text_html(), 'autocomplete': 'new-password'}))
    
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, 
    widget=forms.PasswordInput(attrs=
    {'class': 'form-control', 'autocomplete': 'new-password'}))


class ResetPwdForm(PasswordResetForm):
    email = forms.CharField(label=_("Email"), max_length=254, 
    widget=forms.EmailInput(attrs=
    {'class': 'form-control', 'autocomplete': 'email'}))
    
    
class SetPwdForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, 
    widget=forms.PasswordInput(attrs=
    {'class': 'form-control', 'help_text': password_validation.password_validators_help_text_html(), 'autocomplete': 'new-password'}))
    
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, 
    widget=forms.PasswordInput(attrs=
    {'class': 'form-control', 'autocomplete': 'new-password'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
        'locality': forms.TextInput(attrs={'class': 'form-control'}),
        'city': forms.TextInput(attrs={'class': 'form-control'}),
        'state': forms.Select(attrs={'class': 'form-control'}),
        'zipcode': forms.NumberInput(attrs={'class': 'form-control'})}