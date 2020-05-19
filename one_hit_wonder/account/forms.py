from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Advertisement, Location


# Create a new form class that inherits from the Django UserCreationForm
class UserRegisterForm(UserCreationForm):
    # This allows us to add the email field to the form
    email = forms.EmailField()

    # This saves form data to User model when form.save() method is called
    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2']

# class for the Create Ad form
class LocationSubform(ModelForm):
    class Meta:
        model = Location
        fields = ['city', 'state', 'zip_code']

# class for the Create Ad form
class CreateAdForm(ModelForm):
    class Meta:
        model = Advertisement
        fields = ['instrument']