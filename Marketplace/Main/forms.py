from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from Product.models import Users

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Your Username",
        "class":"form-control form-control-lg"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder":"Your Password",
        "class":"form-control form-control-lg"
    }))


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={
        "placeholder":"Your Email",
        "class":"form-control form-control-lg"
    }))

    class Meta:
        model = Users
        fields = ('username','email','password1','password2','first_name','last_name')
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Your First Name",
        "class":"form-control form-control-lg"
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Your Last Name",
        "class":"form-control form-control-lg"
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Your Username",
        "class":"form-control form-control-lg"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder":"Your Password",
        "class":"form-control form-control-lg"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder":"Repeat Your Password",
        "class":"form-control form-control-lg"
    }))