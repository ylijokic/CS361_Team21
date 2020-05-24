from django.contrib import messages as msgs
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from .forms import UserRegisterForm, MusicianProfileForm, InstrumentSubform, LocationSubform
from .models import Musician, Location, Instrument

posts = [
    {
        'musician': 'Steve S',
        'title': 'Profile Post 1',
        'content': 'First post',
        'date_posted': 'May 3rd, 2020'
    },
]


def landing(request):
    return render(request, 'account/landing.html')


# Decorator to check if user is logged in before displaying profile
@login_required
def home(request):
    context = {
        'posts': posts,
    }
    if profile_is_incomplete(request.user):
        context['incomplete'] = True
        context['musician_form'] = MusicianProfileForm()
        context['location_form'] = LocationSubform()
        context['instrument_form'] = InstrumentSubform()
    return render(request, 'account/home.html', context)


# Decorator to check if user is logged in before displaying profile
@login_required
def profile(request):
    if profile_is_incomplete(request.user):
        return redirect('account-home')

    return render(request, 'account/profile.html', {'title': 'Profile'})


# Decorator to check if user is logged in before displaying profile
@login_required
def messages(request):
    if profile_is_incomplete(request.user):
        return redirect('account-home')

    return render(request, 'account/messages.html', {'title': 'Messages'})


# Decorator to check if user is logged in before displaying profile
@login_required
def matches(request):
    if profile_is_incomplete(request.user):
        return redirect('account-home')

    return render(request, 'account/matches.html', {'title': 'Matches'})


# Decorator to check if user is logged in before displaying profile
@login_required
def create_ad(request):
    if profile_is_incomplete(request.user):
        return redirect('account-home')

    return render(request, 'account/create_ad.html', {'title': 'Create Ad'})


def register(request):
    # Check if the registration form request is a POST request
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # Verify registration form has valid input
        if form.is_valid():
            # Adds user to django admin page
            form.save()
            username = form.cleaned_data.get('username')
            msgs.success(request, f"Account created for {username}")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})


def update_profile(request):
    # Check if the profile update form request is a POST request
    if request.method == 'POST':
        musician_form = MusicianProfileForm(request.POST)
        location_form = LocationSubform(request.POST)
        instrument_form = InstrumentSubform(request.POST)
        # Verify profile form has valid input
        if musician_form.is_valid() and location_form.is_valid() and instrument_form.is_valid():
            musician_location, location_created = Location.objects.get_or_create(**location_form.cleaned_data)
            musician_instrument, instrument_created = Instrument.objects.get_or_create(**instrument_form.cleaned_data)
            try:
                musician = Musician.objects.get(user=request.user)
                musician.location = musician_location
                musician.instruments.set([musician_instrument])
                musician.looking_for_work = musician_form.cleaned_data.get('looking_for_work')
                musician.image = musician_form.cleaned_data.get('image')
            except ObjectDoesNotExist:
                musician, musician_created = Musician.objects.get_or_create(**musician_form.cleaned_data, user=request.user, location=musician_location)
            musician.instruments.set([musician_instrument])
            msgs.success(request, f"Your profile has been updated.")
            return redirect('account-profile')
    else:
        if profile_is_incomplete(request.user):
            return redirect('account-home')
        musician_form = MusicianProfileForm()
        location_form = LocationSubform()
        instrument_form = InstrumentSubform()
    return render(request, 'account/complete_profile.html', {
        'musician_form': musician_form,
        'location_form': location_form,
        'instrument_form': instrument_form
    })


def profile_is_incomplete(user):
    return not hasattr(user, 'musician') or user.musician.looking_for_work is None
