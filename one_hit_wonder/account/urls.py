from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.landing, name='account-landing'),
    path('home/', views.home, name='account-home'),
    path('profile/', views.profile, name='account-profile'),
    path('profile/update/', views.update_profile, name='account-profile-update'),
    path('messages/', views.messages, name='account-messages'),
    path('matches/', views.matches, name='account-matches'),
    path('matches/<str:state>/<str:instrument>', views.matches, name='account-matches'),
    path('create_ad/', views.create_ad, name='account-create_ad'),
    path('update_ad/<str:pk>', views.update_ad, name='account-update_ad'),
    path('delete_ad/<str:pk>', views.delete_ad, name='account-delete_ad'),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="account/logout.html"), name="logout"),
]

# For use during debugging. Change settings for live deployment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
