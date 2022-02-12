from django.shortcuts import render
import requests
import json
from pprint import pprint

from django.http import HttpResponse
from .models import Itinerary, TripEvent
from .serializers import ItinerarySerializer, TripEventSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, mixins
from rest_framework import status

from .permissions import IsOwnerOrReadOnly, IsAdmin, IsOwnerOrAdmin, IsTripEventOwnerOrAdminCreate, IsTripEventOwnerOrAdminUpdate


OPENTRIPMAP_APIKEY = "5ae2e3f221c38a28845f05b67692ad3e6018090b4af24d1fc0c6f08d"
OPENTRIPMAP_API_ENDPOINT = "http://api.opentripmap.com/0.1/en/places"
API_PREFIX = "apikey="
"""
API Helper functions
"""
def object_API(xid):
    """
    xid is the [unique] object ID for each attraction point from OpenTripMap API
    """
    return f"{OPENTRIPMAP_API_ENDPOINT}/xid/{xid}?{API_PREFIX}{OPENTRIPMAP_APIKEY}"

def loc_API(lon, lat, radius=3000):
    """
    radius in meters, default=3000m (3km)
    """
    return f"{OPENTRIPMAP_API_ENDPOINT}/radius?radius={radius}&lon={lon}&lat={lat}&{API_PREFIX}{OPENTRIPMAP_APIKEY}"

"""
search API Endpoints
"""
def search_object(request):
    """
    EXPECT:
        Get Request coming with a header field:
            xid: <string>
    EXAMPLE: 
        curl http://localhost:8000/trip/search/id -H "xid: Q372040"
    """
    headers = request.headers
    xid = headers['xid']
    resp = requests.get(object_API(xid))

    pprint(json.loads(resp.content))
    return  HttpResponse(resp, content_type='application/json')

def search_geoname(request):
    pass

def search_loc(request):
    """
    EXPECT:
        GET Request coming with two header fields:
            lon: <float> (-180, 180)
            lat: <float> (-90, 90)
    EXAMPLE: 
        curl http://localhost:8000/trip/search/loc -H "lon: -118.4464" -H "lat: 34.0651"
    RETURN:
        JSON file containing all attractions within 3km around <lon> and <lat>
    """
    headers = request.headers
    lon = float(headers['lon'])
    lat = float(headers['lat'])
    resp = requests.get(loc_API(lon, lat))

    pprint(json.loads(resp.content))
    return HttpResponse(resp, content_type='application/json')

def search_suggest(request):
    pass


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

    def get_queryset(self):
        return Itinerary.objects.filter(user=self.request.user)


class ItineraryListAll(generics.ListAPIView):
    """
    List all Itinerary of Logged In User
    """
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdmin]


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
    

