"""lazytrip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from User.views import GoogleLogin
from allauth.socialaccount.providers.google import views as google_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homepage'),
    path('user/', include('User.urls')),
    path('trip/', include('Trip.urls')),
    # rest-auth
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    # user registration/login using backend template (depreciated)
    # path('auth/', include('allauth.urls')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/google/callback/', GoogleLogin.google_callback, name='google_callback'),
    path('auth/google/url/', google_views.oauth2_login)
]
