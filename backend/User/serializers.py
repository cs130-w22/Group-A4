from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import UserProfile
from django.contrib.auth.models import User # for extending django User Model


"""
UserSerializer serializes default Django User Model, and will be nested in UserProfile (which
    adds extra information to default Django User Model)
"""
class UserSerializer(WritableNestedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login')


"""
UserProfileSerializer serializes UserProfile Model, which contains Django User Model + 
    additional information (such as bio).
"""
class UserProfileSerializer(WritableNestedModelSerializer):

    # nested serializer for default Django User Model
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'age', 'bio', 'location')


