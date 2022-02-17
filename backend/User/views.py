from cmath import log
import requests
from pprint import pprint
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, mixins

import urllib.parse
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.shortcuts import redirect
from django.urls import reverse

from .serializers import UserProfileSerializer, UserSerializer
from .models import User
from .permissions import IsOwnerOrReadOnly, IsAdmin, IsOwnerOrAdmin
from django.contrib.auth.models import User


# admin user CRUD (all user available)
class UserList(generics.ListAPIView):
    """
    View list of all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdmin]

class UserDetailUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    # support PATCH (update current user profile)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

class UserUpdate(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    # support PATCH (update current user profile)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# regular user CRUD (current logged-in user available)
class CurrentUserDetail(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    # support GET (current user profile)
    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# TODO: make /user/profile/update/ work!
class CurrentUserUpdate(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def perform_update(self, serializer):
        print("[[[PERFORMING UPDATEING>>>>")
        # queryset = User.objects.filter(user=self.request.user)
        serializer.save(id=self.request.user)

    # support PATCH (update current user profile)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

"""
Google OAuth Related
"""
class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):

    access_token_url = "https://accounts.google.com/o/oauth2/token"
    authorize_url = "https://accounts.google.com/o/oauth2/auth"
    profile_url = "https://www.googleapis.com/oauth2/v1/userinfo"

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(
            self.profile_url,
            params={"access_token": token.token, "alt": "json"},
        )
        resp.raise_for_status()
        extra_data = resp.json()
        pprint(extra_data)
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login

class GoogleLogin(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
    # callback_url = "http://localhost:8080/"
    client_class = OAuth2Client

class GoogleCallBack(APIView):
    def get(self, request):
        resp = {
            "Login": "Successful!"
        }
        return HttpResponse(resp, content_type='application/json')

"""
Types of generic class based views: 
CreateAPIView
ListAPIView
RetrieveAPIView
DestroyAPIView
UpdateAPIView
ListCreateAPIView
RetrieveUpdateAPIView
RetrieveDestroyAPIView
RetrieveUpdateDestroyAPIView
"""

# User CRUD (function based views, DEPRICATED!)
@api_view(['GET'])
def list_users(request):
    users = UserProfile.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def view_user(request, pk):
    users = UserProfile.objects.get(id=pk)
    serializer = UserProfileSerializer(users, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = UserProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def update_user(request, pk):
    user = UserProfile.objects.get(id=pk)
    serializer = UserProfileSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
    
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_user(request, pk):
    user = UserProfile.objects.get(id=pk)
    user.delete()

    return Response(f"{pk} successfully deleted!")
