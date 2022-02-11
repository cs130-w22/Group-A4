from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
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


# User CRUD (generic class based views)
class UserList(generics.ListAPIView):
    """
    View list of all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdmin]

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

class UserUpdate(generics.GenericAPIView, mixins.UpdateModelMixin):
# class UserUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]



class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # callback_url = "http://localhost:8000/allauth/google/login/callback/"
    client_class = OAuth2Client

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
