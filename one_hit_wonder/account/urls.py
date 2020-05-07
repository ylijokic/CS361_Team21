from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='account-landing'),
    path('home/', views.home, name='account-home'),
    path('profile/', views.profile, name='account-profile'),
    path('messages/', views.messages, name='account-messages'),
    path('matches/', views.matches, name='account-matches'),
    path('create_ad/', views.create_ad, name='account-create_ad'),
]

