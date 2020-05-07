from django.shortcuts import render
from django.contrib.auth.decorators import login_required

posts = [
    {
        'musician': 'Steve S',
        'title': 'Profile Post 1',
        'content': 'First post',
        'date_posted': 'May 3rd, 2020'
    },
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'account/home.html', context)

# Decorator to check if user is logged in before displaying profile
@login_required
def profile(request):
    return render(request, 'account/profile.html', {'title': 'Profile'})

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
