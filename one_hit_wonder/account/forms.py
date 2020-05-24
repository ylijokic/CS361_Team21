from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Musician, Instrument, Location


# Create a new form class that inherits from the Django UserCreationForm
class UserRegisterForm(UserCreationForm):
    # This allows us to add the email field to the form
    email = forms.EmailField()

    # This saves form data to User model when form.save() method is called
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)


class MusicianProfileForm(ModelForm):
    class Meta:
        model = Musician
        fields = ('image', 'looking_for_work',)
        labels = {
            'looking_for_work': 'I want to join a band',
            'image': 'Profile Picture',
        }


# class for the Profile Completion form
class InstrumentSubform(ModelForm):
    class Meta:
        model = Instrument
        fields = '__all__'
        labels = {
            'name': 'Primary Instrument',
        }


# class for the Create Ad form and Profile Completion form
class LocationSubform(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        labels = {
            'zip_code': 'ZIP Code',
        }
