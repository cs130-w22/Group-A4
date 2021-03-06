from Trip.models import Itinerary
from Trip.serializers import ItinerarySerializer
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer, NestedUpdateMixin

from .models import UserProfile
from django.contrib.auth.models import User # for extending django User Model


"""
UserProfileSerializer serializes UserProfile Model, which contains Django User Model + 
    additional information (such as bio).
"""
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('age', 'bio', 'location')


"""
UserSerializer serializes default Django User Model, and will be nested in UserProfile (which
    adds extra information to default Django User Model)
"""
class UserSerializer(WritableNestedModelSerializer):
    # for the use of Foreign Key relationship between Itinerary and Use (https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/)
    # itinerary = serializers.PrimaryKeyRelatedField(many=True, queryset=Itinerary.objects.all())
    itinerary = ItinerarySerializer(many=True, read_only=True)

    # nested serializer for default Django User Model
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'profile', 'itinerary')






