from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignupForm(UserCreationForm):
    """
    Custom form for user registration, inheriting from Django's UserCreationForm.
    """
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_photo']

class LoginForm(AuthenticationForm):
    """
    Custom login form inheriting from Django's AuthenticationForm.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating the user's profile information.
    """
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_photo']
