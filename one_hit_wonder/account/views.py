from django.shortcuts import render

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

def profile(request):
    return render(request, 'account/profile.html', {'title': 'Profile'})

def messages(request):
    return render(request, 'account/messages.html', {'title': 'Messages'})

def matches(request):
    return render(request, 'account/matches.html', {'title': 'Matches'})

def create_ad(request):
    return render(request, 'account/create_ad.html', {'title': 'Create Ad'})
