from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'account/home.html')

def profile(request):
    return render(request, 'account/profile.html')

def messages(request):
    return render(request, 'account/messages.html')

def matches(request):
    return render(request, 'account/matches.html')

def create_ad(request):
    return render(request, 'account/create_ad.html')
