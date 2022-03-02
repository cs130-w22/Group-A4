from xml.dom import ValidationErr
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import exceptions

from .models import Itinerary, TripEvent
from User.models import User



"""
TripEventSerializer serializes TripEvent Model, used as the smallest scheduling unit.
"""
class TripEventSerializer(WritableNestedModelSerializer):
    # nested serializer for Itinerary model
    itin = Itinerary

    class Meta:
        model = TripEvent
        fields = ('id', 'place_id', 'place_name', 'start_time', 'end_time', 'itin', 'lat', 'lng', 'place_json')

    # def validate(self, data):
    #     print("\n\n[[[[[[Calling validate() Method...]]]]]]\n\n")
    #     itin_id = data.pop('itin_id')
    #     try:
    #         Itinerary.objects.get(id=itin_id)
    #     except ValidationErr:
    #         raise exceptions.ValidationError(detail="Itinerary does not exists, only able to associate TripEvent with existing itinerary!")
    #     return data

    # def create(self, validated_data):
    #     # handle foreign key creation
    #     print("\n\n[[[[[[Calling save() Method...]]]]]]\n\n")
    #     itin_id = validated_data.pop('itin_id')
    #     itin_instance = Itinerary.objects.get(id=itin_id)
    #     tripevent_instance = TripEvent.objects.create(**validated_data, itin=itin_instance)
    #     return tripevent_instance

"""
ItinerarySerializer serializes Itinerary Model, consists of 0 or more TripEvent
"""
class ItinerarySerializer(WritableNestedModelSerializer):
    # nested serializer for Itinerary model
    user = serializers.ReadOnlyField(source='user.id')
    trip_event = TripEventSerializer(many=True, read_only=True)

    # itinerary = serializers.PrimaryKeyRelatedField(many=True, queryset=Itinerary.objects.all())

    class Meta:
        model = Itinerary
        fields = ('id', 'title', 'desc', 'created_at', 'last_modified', 'user', 'trip_event')
    