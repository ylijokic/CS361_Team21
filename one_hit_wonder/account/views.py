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
    return render(request, 'account/profile.html')

def messages(request):
    return render(request, 'account/messages.html')

def matches(request):
    return render(request, 'account/matches.html')

def create_ad(request):
    return render(request, 'account/create_ad.html')
