from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as user_views
from account import views as account_views

urlpatterns = [
    path('', account_views.home, name='account-landing'),
    path('home/', account_views.home, name='account-home'),
    path('profile/', user_views.profile, name='users-profile'),
    path('messages/', account_views.messages, name='account-messages'),
    path('matches/', account_views.matches, name='account-matches'),
    path('create_ad/', account_views.create_ad, name='account-create_ad'),
]

#For use during debugging. Change settings for live deployment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)