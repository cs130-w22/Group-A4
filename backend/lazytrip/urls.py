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
from User import views as user_views
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

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
    path('auth/google/', user_views.GoogleLogin.as_view(), name='google_login'),
    path('auth/google/callback/', OAuth2CallbackView.adapter_view(GoogleOAuth2Adapter), name='google_callback'),
]
