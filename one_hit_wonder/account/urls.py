from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='account-home'),
    path('profile/', views.profile, name='account-profile'),
    path('messages/', views.messages, name='account-messages'),
    path('matches/', views.matches, name='account-matches'),
    path('create_ad/', views.create_ad, name='account-create_ad'),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="account/logout.html"), name="logout"),
]

