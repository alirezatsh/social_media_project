from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegisterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField( widget= forms.EmailInput(attrs={'placeholder' : 'please enter the email'}) )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Please enter your password'}))
    password2 = forms.CharField( label= 'confirmpass' , widget=forms.PasswordInput(attrs={'placeholder' : 'Please enter your password'}))

    
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists')
        return email
            
            
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username already exists')
        
        return username
    
    
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2') 
        
        if p1 and p2 and p1 != p2:
            raise ValidationError('passwords must match')
        
        
class USerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Please enter your password'}))
    
    
    
class EditUserProfile(forms.ModelForm):
    
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ('age' , 'bio')
