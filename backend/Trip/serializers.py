from xml.dom import ValidationErr
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import exceptions

from .models import Itinerary, TripEvent
from User.models import User


"""
ItinerarySerializer serializes Itinerary Model, consists of 0 or more TripEvent
"""
class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    # nested serializer for Itinerary model
    user = serializers.ReadOnlyField(source='user.id')

    # itinerary = serializers.PrimaryKeyRelatedField(many=True, queryset=Itinerary.objects.all())

    class Meta:
        model = Itinerary
        fields = ('id', 'title', 'desc', 'created_at', 'last_modified', 'user')
    

"""
UserProfileSerializer serializes UserProfile Model, which contains Django User Model + 
    additional information (such as bio).
"""
class TripEventSerializer(serializers.HyperlinkedModelSerializer):
    # nested serializer for Itinerary model
    itin = Itinerary

    class Meta:
        model = TripEvent
        fields = ('xid', 'start_time', 'end_time', 'itin')

    def validate(self, data):
        print("\n\n[[[[[[Calling validate() Method...]]]]]]\n\n")
        itin_id = data.pop('itin_id')
        try:
            Itinerary.objects.get(id=itin_id)
        except ValidationErr:
            raise exceptions.ValidationError(detail="Itinerary does not exists, only able to associate TripEvent with existing itinerary!")
        return data

    def create(self, validated_data):
        # handle foreign key creation
        print("\n\n[[[[[[Calling save() Method...]]]]]]\n\n")
        itin_id = validated_data.pop('itin_id')
        itin_instance = Itinerary.objects.get(id=itin_id)
        tripevent_instance = TripEvent.objects.create(**validated_data, itin=itin_instance)
        return tripevent_instance

