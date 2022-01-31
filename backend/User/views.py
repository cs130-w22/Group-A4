from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions, mixins

from .serializers import UserProfileSerializer
from .models import UserProfile
from .permissions import IsOwnerOrReadOnly

# User CRUD (generic class based views)
class UserList(generics.ListAPIView):
    """
    View list of all users
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserUpdate(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserDelete(generics.DestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


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
