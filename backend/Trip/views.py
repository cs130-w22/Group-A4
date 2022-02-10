from django.shortcuts import render
import requests
import json
from pprint import pprint

from django.http import HttpResponse
from rest_framework.response import Response

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
View functions
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
