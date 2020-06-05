from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Advertisement, Musician, Instrument, Location, Video


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
        fields = ('image', 'looking_for_work', 'phone', 'twitter', 'instagram')
        labels = {
            'looking_for_work': 'I want to join a band',
            'image': 'Profile Picture',
            'phone': 'Phone Number',
            'twitter': 'Twitter',
            'instagram': 'Instagram',
        }


# class for the Profile Completion form
class InstrumentSubform(ModelForm):
    class Meta:
        model = Instrument
        fields = '__all__'
        labels = {
            'name': 'Primary Instrument',
        }


STATES = (
    ('', 'Choose...'),
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)


# class for the Create Ad form and Profile Completion form
class LocationSubform(ModelForm):
    state = forms.ChoiceField(choices=STATES)

    class Meta:
        model = Location
        fields = '__all__'
        labels = {
            'zip_code': 'ZIP Code',
        }


class VideoSubform(ModelForm):
    class Meta:
        model = Video
        fields = '__all__'
        labels = {
            'video': 'Work sample (e.g., YouTube video, SoundCloud link)',
        }

        
# class for the Create Ad form
class CreateAdForm(ModelForm):
    class Meta:
        model = Advertisement
        fields = ['position_filled', 'instrument']
        labels = {
            'position_filled': 'Is the position already filled?'
        }
