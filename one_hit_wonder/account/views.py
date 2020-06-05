from django.contrib import messages as msgs
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

from .forms import UserRegisterForm, CreateAdForm, MusicianProfileForm, InstrumentSubform, LocationSubform, VideoSubform, SearchAdForm, StateSubform
from .models import Musician, Location, Instrument, Advertisement, Video
from .config import api_key

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
        context['video_form'] = VideoSubform()
    return render(request, 'account/home.html', context)


# Decorator to check if user is logged in before displaying profile
@login_required
def profile(request):
    if profile_is_incomplete(request.user):
        return redirect('account-home')

    # Grab the variables needed for Profile Page
    location = request.user.musician.location
    instruments = request.user.musician.instruments.get().name
    skill = request.user.musician.instruments.get().skill_level
    work = request.user.musician.looking_for_work
    videos = request.user.musician.videos.all()
    phone = request.user.musician.phone
    twitter = request.user.musician.twitter
    instagram = request.user.musician.instagram
    ads = Advertisement.objects.filter(creator=request.user.musician.id)

    accessToken = api_key
    context = {
        'title': 'Profile',
        'location': location,
        'instruments': instruments,
        'skill': range(skill),
        'work': work,
        'videos': videos,
        'phone': phone,
        'twitter': twitter,
        'instagram': instagram,
        'accessToken': accessToken,
        'ads': ads  # Query ads and filter for the current user
    }
    return render(request, 'account/profile.html', context)

# View to display other user's profile
@login_required
def profile_other(request, pk):
    if profile_is_incomplete(request.user):
        return redirect('account-home')

    musician = Musician.objects.get(id=pk)

    # Grab the variables needed for Profile Page
    location = musician.location
    instruments = musician.instruments.get().name
    skill = musician.instruments.get().skill_level
    work = musician.looking_for_work
    videos = musician.videos.all()
    phone = musician.phone
    twitter = musician.twitter
    instagram = musician.instagram

    accessToken = api_key
    context = {
        'title': 'Profile',
        'user': musician.user,
        'location': location,
        'instruments': instruments,
        'skill': range(skill),
        'work': work,
        'videos': videos,
        'phone': phone,
        'twitter': twitter,
        'instagram': instagram,
        'accessToken': accessToken,
        'other': True,
    }
    return render(request, 'account/profile.html', context)

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

    form = SearchAdForm()
    subform = StateSubform()

    if request.method == 'POST' :
        subform = StateSubform(request.POST)
        instance = subform.save(commit=False)
        if hasattr(instance, 'state'):
            state = instance.state
            SearchAdForm
            ads = Advertisement.objects.filter(position_filled=False, location__state=state)
        form = SearchAdForm(request.POST)
        instance = form.save(commit=False)
        if hasattr(instance, 'instrument'):
            instrument = instance.instrument
            ads = Advertisement.objects.filter(position_filled=False, instrument__name=instrument.name)
        if hasattr(instance, 'state') and hasattr(instance, 'instrument'):
            ads = Advertisement.objects.filter(position_filled=False, location__state=state, instrument__name=instrument.name)
    else:
        ads = Advertisement.objects.filter(position_filled=False).order_by('location__state', 'instrument__name')

    return render(request, 'account/matches.html', { 'form': form, 'subform': subform, 'ads': ads})


@login_required
def create_ad(request):
    if profile_is_incomplete(request.user):
        return redirect('account-home')

    if request.method == 'POST':
        # main form
        form = CreateAdForm(request.POST)
        # subform for location
        location_form = LocationSubform(request.POST)
        # subform for instrument
        instrument_form = InstrumentSubform(request.POST)
        # check if all inputs are correct
        if form.is_valid() and location_form.is_valid() and instrument_form.is_valid():
            # delay the save for the main form
            instance = form.save(commit=False)
            # save the location
            ad_location, location_created = Location.objects.get_or_create(**location_form.cleaned_data)
            # save the instrument
            ad_instrument, instrument_created = Instrument.objects.get_or_create(**instrument_form.cleaned_data)
            instance.location = ad_location
            instance.instrument = ad_instrument
            # the creator is the current user
            instance.creator = request.user.musician
            # add new ad to the database
            instance.save()
            msgs.success(request, f"New ad created successfully")
            return redirect(profile)
    else:
        form = CreateAdForm()
        location_form = LocationSubform()
        instrument_form = InstrumentSubform()
    return render(request, 'account/create_ad.html', {'action': 'Create New',
                                                      'title': 'Create Advertisement',
                                                      'form': form,
                                                      'location_form': location_form,
                                                      'instrument_form': instrument_form
                                                      })


@login_required
def update_ad(request, pk):
    ad = Advertisement.objects.get(id=pk)
    form = CreateAdForm(instance=ad)

    if request.method == 'POST':
        # main form
        form = CreateAdForm(request.POST, instance=ad)
        # subform for location
        location_form = LocationSubform(request.POST, instance=ad.location)
        # subform for instrument
        instrument_form = InstrumentSubform(request.POST, instance=ad.instrument)
        # check if all inputs are correct
        if form.is_valid() and location_form.is_valid() and instrument_form.is_valid():
            # delay the save for the main form
            instance = form.save(commit=False)
            # save the location
            ad_location, location_created = Location.objects.get_or_create(**location_form.cleaned_data)
            # save the instrument
            ad_instrument, instrument_created = Instrument.objects.get_or_create(**instrument_form.cleaned_data)
            instance.location = ad_location
            instance.instrument = ad_instrument
            # the creator is the current user
            instance.creator = request.user.musician
            # add new ad to the database
            instance.save()
            msgs.success(request, f"Ad updated successfully")
            return redirect(profile)
    else:
        form = CreateAdForm(instance=ad)
        location_form = LocationSubform(instance=ad.location)
        instrument_form = InstrumentSubform(instance=ad.instrument)
    return render(request, 'account/create_ad.html', {'action': 'Update',
                                                      'title': 'Update Advertisement',
                                                      'form': form,
                                                      'location_form': location_form,
                                                      'instrument_form': instrument_form
                                                      })


@login_required
def delete_ad(request, pk):
    ad = Advertisement.objects.get(id=pk)

    context = {'ad': ad}

    if request.method == 'POST':
        ad.delete()
        msgs.success(request, f"Ad deleted successfully")
        return redirect(profile)

    return render(request, 'account/delete_ad.html', context)


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
    # Check if the profile update form request is a POST request.
    if request.method == 'POST':
        # Get the data submitted in the three combined forms.
        musician_form = MusicianProfileForm(request.POST)
        location_form = LocationSubform(request.POST)
        instrument_form = InstrumentSubform(request.POST)
        video_form = VideoSubform(request.POST)
        # Verify all forms have valid input.
        if musician_form.is_valid() and location_form.is_valid() and instrument_form.is_valid() and video_form.is_valid():
            # Create the location and instrument entered by the user,
            # or locate matching instances in the database.
            musician_location, location_created = Location.objects.get_or_create(**location_form.cleaned_data)
            musician_instrument, instrument_created = Instrument.objects.get_or_create(**instrument_form.cleaned_data)
            musician_video, video_created = Video.objects.get_or_create(**video_form.cleaned_data)

            try:
                # If the user is being updated, find the user's musician data,
                # then update it with the information from the form.
                musician = Musician.objects.get(user=request.user)
                musician.location = musician_location
                musician.instruments.set([musician_instrument])
                musician.videos.add(musician_video)
                musician.looking_for_work = musician_form.cleaned_data.get('looking_for_work')
                musician.image = musician_form.cleaned_data.get('image')
                musician.phone = musician_form.cleaned_data.get('phone')
                musician.twitter = musician_form.cleaned_data.get('twitter')
                musician.instagram = musician_form.cleaned_data.get('instagram')
                musician.save()
            except ObjectDoesNotExist:
                # If the user's musician profile wasn't completed yet, create a musician object based off of the forms,
                # then associate the musician object with the user.
                musician, musician_created = Musician.objects.get_or_create(
                    **musician_form.cleaned_data,
                    user=request.user,
                    location=musician_location)
                musician.instruments.set([musician_instrument])
                musician.videos.add(musician_video)
                musician.save()
            msgs.success(request, f"Your profile has been updated.")
            return redirect('account-profile')
    else:
        # If the user is trying to update the musician profile before completing it,
        # redirect the user back to the homepage to display the form in a modal.
        if profile_is_incomplete(request.user):
            return redirect('account-home')
        # If the user has a completed musician profile, get their current information so we can pre-populate the forms.
        current_location = Musician.objects.get(user=request.user).location
        current_instrument = Musician.objects.get(user=request.user).instruments.all()[0]

        musician_form = MusicianProfileForm(instance=request.user.musician)
        location_form = LocationSubform(initial={
            'city': current_location.city,
            'state': current_location.state,
            'zip_code': current_location.zip_code
        })
        instrument_form = InstrumentSubform(initial={
            'name': current_instrument.name,
            'skill_level': current_instrument.skill_level
        })
        video_form = VideoSubform()
    return render(request, 'account/complete_profile.html', {
        'title': 'Update Profile',
        'musician_form': musician_form,
        'location_form': location_form,
        'instrument_form': instrument_form,
        'video_form': video_form
    })


def profile_is_incomplete(user):
    return not hasattr(user, 'musician') or user.musician.looking_for_work is None
