from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, HouseRental, Business, Post

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class HouseRentalForm(forms.ModelForm):
    class Meta:
        model = HouseRental
        exclude = ('admin',)     

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'hood')   

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'houserental')

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('admin',)