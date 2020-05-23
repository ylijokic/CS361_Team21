from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as msgs
from django.views.generic import TemplateView
from .forms import UserRegisterForm, CreateAdForm, LocationSubform
from .models import Musician, Advertisement

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
    ads = Advertisement.objects.filter(creator=request.user.musician.id)
    print(ads)
    context = {
        'title': 'Profile',
        'ads': ads
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


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = CreateAdForm(request.POST)
        subform = LocationSubform(request.POST)
        if form.is_valid() and subform.is_valid():
            instance = form.save(commit=False)
            instance.position_filled = False
            instance.location = subform.save()
            instance.creator_id = request.user.musician.id
            instance.save()
            msgs.success(request, f"New ad created successfully")
            return redirect(create_ad)
    else:
        form = CreateAdForm()
        subform = LocationSubform()
    return render(request, 'account/create_ad.html', {'form': form, 'subform': subform})


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
