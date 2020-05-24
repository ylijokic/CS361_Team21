from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as msgs
from .forms import UserRegisterForm
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
    print(request)
    return render(request, 'account/landing.html')


# Decorator to check if user is logged in before displaying profile
@login_required
def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'account/home.html', context)


# Decorator to check if user is logged in before displaying profile
@login_required
def profile(request):
    # Grab the variables needed for Profile Page
    location = request.user.musician.location
    instruments = request.user.musician.instruments.get().name
    skill = request.user.musician.instruments.get().skill_level
    work = request.user.musician.looking_for_work
    videos = request.user.musician.videos.all()
    
    accessToken = api_key
    context = {
        'title': 'Profile',
        'location': location,
        'instruments': instruments,
        'skill': range(skill),
        'work': work,
        'videos': videos,
        'accessToken': accessToken
    }
    return render(request, 'account/profile.html', context)


# Decorator to check if user is logged in before displaying profile
@login_required
def messages(request):
    return render(request, 'account/messages.html', {'title': 'Messages'})


# Decorator to check if user is logged in before displaying profile
@login_required
def matches(request):
    return render(request, 'account/matches.html', {'title': 'Matches'})


# Decorator to check if user is logged in before displaying profile
@login_required
def create_ad(request):
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
