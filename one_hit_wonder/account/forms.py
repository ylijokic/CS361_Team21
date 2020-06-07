from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Advertisement, Musician, Instrument, Location, Video


# Helper widget to populate existing database entries as well as allow
# custom data entry.
# Source: https://stackoverflow.com/questions/24783275/django-form-with-choices-but-also-with-freetext-option
class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return text_html + data_list


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
    name = forms.CharField(required=True, label='Instrument')

    def __init__(self, *args, **kwargs):
        _instrument_list = kwargs.pop('data_list', None)
        super(InstrumentSubform, self).__init__(*args, **kwargs)
        self.fields['name'].widget = ListTextWidget(data_list=_instrument_list, name='instrument-list')

    class Meta:
        model = Instrument
        fields = '__all__'


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
    city = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        _city_list = kwargs.pop('data_list', None)
        super(LocationSubform, self).__init__(*args, **kwargs)
        self.fields['city'].widget = ListTextWidget(data_list=_city_list, name='city-list')

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
        fields = ('position_filled',)
        labels = {
            'position_filled': 'Is the position already filled?'
        }

# class for the ads search page
class SearchAdForm(ModelForm):
    class Meta:
        model = Advertisement
        fields = ['instrument']

    def __init__(self, *args, **kwargs):
        super(SearchAdForm, self).__init__(*args, **kwargs)
        self.fields['instrument'].required = False

# subfrom for State
class StateSubform(ModelForm):
    state = forms.ChoiceField(choices=STATES)
    class Meta:
        model = Location
        fields = ['state']

    def __init__(self, *args, **kwargs):
        super(StateSubform, self).__init__(*args, **kwargs)
        self.fields['state'].required = False