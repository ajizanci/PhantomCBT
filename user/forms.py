from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=24)
    password = forms.CharField(max_length=24, widget=forms.PasswordInput)
    
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=24)
    password = forms.CharField(max_length=24, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=24, widget=forms.PasswordInput)
    