import json
from datetime import datetime
from collections import defaultdict
from pprint import pprint

from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from .models import Itinerary, TripEvent
from .serializers import ItinerarySerializer, TripEventSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, mixins
from rest_framework import status
from rest_framework.exceptions import ParseError

from .permissions import IsOwnerOrReadOnly, IsAdmin, IsOwnerOrAdmin, IsTripEventOwnerOrAdminCreate, IsTripEventOwnerOrAdminUpdate


"""
TripEvent CRUD API Views
"""
class TripEventCRUD(APIView):
    """
    List all TripEvents in this itinerary, and/or create/update/delete TripEvent
    """
    def get(self, request, format=None):
        TripEvents = Itinerary.tripevent_set.all()
        serializer = TripEventSerializer(TripEvents, many=True)
        print(TripEvents)
        return Response(serializer.data)

    def post(self, request, format=None):
        print("\n\n\n\n\n[RCVD POST REQUEST PARAMS:!!!!]")
        # ensure data validity

        serializer = TripEventSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            print("\n\n\n\n\n[DATA RCVD BELOW]")
            pprint(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
TripEvent CRUD API Views
"""
class TripEventCreate(generics.CreateAPIView):
    """
    Create an Itinerary under logged in user
    """
    queryset = TripEvent.objects.all()
    serializer_class = TripEventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsTripEventOwnerOrAdminCreate]



class TripEventUpdate(generics.UpdateAPIView):
    """
    Create an Itinerary under logged in user
    """
    queryset = TripEvent.objects.all()
    serializer_class = TripEventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsTripEventOwnerOrAdminUpdate]

    # support PATCH (update current user profile)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

"""
Itinerary CRUD API Views
"""
class ItineraryCreate(generics.CreateAPIView):
    """
    Create an Itinerary under logged in user
    """
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ItineraryList(generics.ListAPIView):
    """
    List all Itinerary of Logged In User
    """
    # queryset = Itinerary.objects.get(user=self.request.user)
    serializer_class = ItinerarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def get(self, request):
        all_itineraries = Itinerary.objects.filter(user=self.request.user)
        simplified_itinerary_info = []
        for itinerary in all_itineraries:
            print(itinerary.id)
            info = {}
            info['id'] = itinerary.id
            info['title'] = itinerary.title
            info['last_modified'] = itinerary.last_modified
            simplified_itinerary_info.append(info)

        return HttpResponse(json.dumps(simplified_itinerary_info, cls=DjangoJSONEncoder), content_type='application/json')

    def get_queryset(self):
        return Itinerary.objects.filter(user=self.request.user)


class ItineraryListAll(generics.ListAPIView):
    """
    List all Itinerary of Logged In User
    """
    serializer_class = ItinerarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def get_queryset(self):
        return Itinerary.objects.filter(user=self.request.user)


class ItineraryViewUpdate(generics.RetrieveUpdateAPIView):
    """
    View Itinerary Detail with id=/<int:pk>/
    """
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    # support PATCH (update current user profile)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, pk, wrap_coord=True):
        # group by each date
        try:
            itinerary = Itinerary.objects.get(id=pk)
        except:
            raise ParseError(detail=f"Itinerary id={pk} not found", code=404)
        itinerary_serializer = ItinerarySerializer(itinerary)

        # reorder tripevents into dates
        itinerary_json = itinerary_serializer.data
        date_grouped_table = defaultdict(list)
        for event in itinerary_json['trip_event']:
            # wrap lat/lng as RUOYU HE requested :)
            if wrap_coord:
                event['geometry'] = {
                    'location': {
                        'lat': event['lat'],
                        'lng': event['lng']
                    }
                }
            date = str(datetime.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%S%z").date())
            date_grouped_table[str(date)].append(event)



        # group by date
        itinerary_json['trip_event'] = date_grouped_table

        return Response(itinerary_json)



    
class ItineraryCRUD(generics.RetrieveUpdateDestroyAPIView):
    """
    List all TripEvents in a specific itinerary, and/or update/delete Itinerary
    """
    # def get(self, request, format=None):
    #     print("\n\n\n\n\n[RCVD POST REQUEST DATA:!!!!]")
    #     print(request.data)
    #     print(request.user)
    #     user = request.user
    #     itinerary = Itinerary.objects.filter(user=user)
    #     serializer = ItinerarySerializer(itinerary, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     print("\n\n\n\n\n[RCVD POST REQUEST DATA:!!!!]")
    #     print(request.data)
    #     serializer = ItinerarySerializer(data=request.data)
    #     print(request.user)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         pprint(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

