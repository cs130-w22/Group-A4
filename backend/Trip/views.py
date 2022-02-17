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
from rest_framework.exceptions import ParseError

import googlemaps
from datetime import datetime

from .permissions import IsOwnerOrReadOnly, IsAdmin, IsOwnerOrAdmin, IsTripEventOwnerOrAdminCreate, IsTripEventOwnerOrAdminUpdate


OPENTRIPMAP_APIKEY = "5ae2e3f221c38a28845f05b67692ad3e6018090b4af24d1fc0c6f08d"
OPENTRIPMAP_API_ENDPOINT = "http://api.opentripmap.com/0.1/en/places"
API_PREFIX = "apikey="

GOOGLEMAP_APIKEY = "AIzaSyDrg_oL7B5OjeAVSc92Nye5UqaO2iSBP8k"
gmaps = googlemaps.Client(key=GOOGLEMAP_APIKEY)

"""
API Helper functions
"""
def object_API(xid: str):
    """
    xid is the [unique] object ID for each attraction point from OpenTripMap API
    """
    return f"{OPENTRIPMAP_API_ENDPOINT}/xid/{xid}?{API_PREFIX}{OPENTRIPMAP_APIKEY}"

def loc_API(lon: float, lat: float, cnt: int=-1, radius: int=3000):
    """
    radius in meters, default=3000m (3km)
    """
    limit = ""
    if cnt > 0:
        limit = f"limit{cnt}&"
    return f"{OPENTRIPMAP_API_ENDPOINT}/radius?radius={radius}&lon={lon}&lat={lat}&{limit}{API_PREFIX}{OPENTRIPMAP_APIKEY}"

def getcoord_API(geoname: str, country: str="us"):
    """
    geoname is a string representing the querying location
    country is a string representing the location country, default to U.S.
    """
    return f"{OPENTRIPMAP_API_ENDPOINT}/geoname?name={geoname}&country={country}&{API_PREFIX}{OPENTRIPMAP_APIKEY}"


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

class SearchObject(APIView):
    """
    EXPECT:
        Get Request coming with a JSON entry in data:
            xid: <string>
    EXAMPLE: 
        curl -X GET http://localhost:8000/trip/search/id/ -d "xid"="Q372040"
    """
    def get(self, request, format=None):
        print("[Calling Search LOC API]: ", request.data)
        data = request.data
        try:
            xid = data['xid']
            resp = requests.get(object_API(xid))
            
            pprint(json.loads(resp.content))
            return HttpResponse(resp, content_type='application/json')
        except:
            raise ParseError(detail="Expecting 'xid' field contained in request JSON.", code=None)

class SearchLocation(APIView):
    """
    EXPECT:
        GET Request coming with two JSON entries in data, either have one of these:
            lon: <float> (-180, 180)
            lat: <float> (-90, 90)
        or
            location: <string> 
    EXAMPLE: 
        curl -X GET http://localhost:8000/trip/search/loc/ -d "lon"="-118.4085" -d "lat"="33.9416" 
        (or using name of the location):
        curl -X GET http://localhost:8000/trip/search/loc/ -d "location"="UCLA"
    RETURN:
        JSON file containing all attractions within 3km around <lon> and <lat>
    """
    def __request_on_coord(self, lon: float, lat: float):
        """
        send API request using coordinates (lon, lat)
        """
        try:
            resp = requests.get(loc_API(lon, lat))
            
            pprint(json.loads(resp.content))
            return HttpResponse(resp, content_type='application/json')
        except:
            raise ParseError(detail="Wrong formatting for 'lon' and/or 'lat' field.", code=None)

    def get(self, request, format=None):
        print("[Calling Search LOC API]: ", request.data)
        data = request.data
        if 'lon' in data and 'lat' in data:
            lon = float(data['lon'])
            lat = float(data['lat'])
            return self.__request_on_coord(lon, lat)

        elif 'location' in data:
            try:
                location = data['location']
                # retrieve coordinates from this geolocation
                coord_resp = requests.get(getcoord_API(location))
                
                pprint(json.loads(coord_resp.content))
                coord_resp = json.loads(coord_resp.content)
                if 'lon' not in coord_resp or 'lat' not in coord_resp:
                    raise ParseError(detail="Please use a more detailed location name.", code=None)
                lon = coord_resp['lon']
                lat = coord_resp['lat']

                # retrieve location 
                return self.__request_on_coord(lon, lat)
            except:
                raise ParseError(detail="Wrong formatting for 'location' field.", code=None)
        
        raise ParseError(detail="Expecting either 'lon' and 'lat' field, or 'location' field.", code=None)



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
    

