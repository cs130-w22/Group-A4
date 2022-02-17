import googlemaps
from pprint import pprint
from datetime import datetime

from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from django.http import HttpResponse

# API GUIDE: 
# https://github.com/googlemaps/google-maps-services-python
# https://github.com/googlemaps/google-maps-services-python/blob/4dd8db6b53049869cf98f2fed3ba8e56676d1709/googlemaps/places.py


# CONFIG
LANGUAGE = "en-US"
GOOGLEMAP_APIKEY = "AIzaSyDrg_oL7B5OjeAVSc92Nye5UqaO2iSBP8k"
GOOGLEMAP_PHOTO_API = "https://maps.googleapis.com/maps/api/place/photo?"
gmaps = googlemaps.Client(key=GOOGLEMAP_APIKEY)
# SEARCH CONFIG
ATTRACTION_TYPES = [
    # "amusement_park",
    # "aquarium",
    # "art_gallery",
    # "campground",
    # "casino",
    # "hindu_temple",
    # "library",
    # "mosque",
    # "movie_theater",
    # "museum",
    # "night_club",
    # "park",
    # "shopping_mall",
    # "stadium",
    # "synagogue",
    "tourist_attraction", # actually includes lots of other types
    # "university",
    # "zoo"
]
RADIUS = 100000

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
    def __get_coord_by_name(self, name:str):
        print(f"Getting coordinates of queried place: {name}")
        resp =  gmaps.find_place(
            name,
            "textquery",
            fields=["place_id", "name", "geometry/location"],
            language=LANGUAGE,
        )
        try:
            candidate = resp['candidates'][0]
            # coord in (lat, lng)
            coord = (candidate['geometry']['location']['lat'], candidate['geometry']['location']['lng'])
            return coord
        except:
            ParseError(detail=f"Cannot find places named [{name}]", code=None)

    def __find_places_in_radius(self, coord: tuple[float, float], radius:int=10000, min_price=None, max_price=None, rank_by=None, type=None):
        """
        find places within [radius] (in meters) from [coord]
        """
        resp = gmaps.places_nearby(
            # "textquery",
            location=coord,
            radius=radius,
            min_price=min_price,
            max_price=max_price,
            rank_by=rank_by,    # default by prominance, can also take 'distance'
            type=type,          # type supported: https://developers.google.com/maps/documentation/places/web-service/supported_types
            language=LANGUAGE,
        )

        return resp['results']

    def __get_photo_url(self, ref:str, max_width:int=300):
        """
        get a url to photo using photo reference (got from place or place detail)
        """
        photo_url = f"{GOOGLEMAP_PHOTO_API}maxwidth={max_width}&photoreference={ref}&key={GOOGLEMAP_APIKEY}"
        return photo_url

    def get(self, request, format=None):
        # retrieving data
        data = request.data
        # sanity checks
        if not 'location' in data:
            raise ParseError(detail="Expecting a string field 'location' indicating the destination for recommendation.", code=None)

        location = data['location']
        # get coordinates based on name of the places (lat, lng)
        coord = self.__get_coord_by_name(location)

        # NOTE: because google map api only support 1 type restriction per query,
        #       so need to send 1 request per place's type.
        nearby_places = []
        for TYPE in ATTRACTION_TYPES:
            print(f"Searching for TYPE = {TYPE}...")
            # use the coordinates to retrieve nearby places of interests
            nearby_places.extend(self.__find_places_in_radius(coord, radius=RADIUS, type=TYPE))

        # pprint(nearby_places)
        print(f"Found {len(nearby_places)} places {RADIUS}m around {location}")

        filtered_places = []
        # pprint(nearby_places[:])
        # filter information for all places queried
        
        for place in nearby_places:
            place_json = {}
            # place id
            place_json['place_id'] = place['place_id']
            # place name
            place_json['name'] = place['name']
            # photo url
            if 'photos' in place:
                photo_ref = place['photos'][0]['photo_reference']
                photo_url = self.__get_photo_url(photo_ref)
                place_json['photo_url'] = photo_url
            # rating
            if 'rating' in place:
                place_json['rating'] = place['rating']
            # longitude/latitude
            lng = place['geometry']['location']['lng']
            lat = place['geometry']['location']['lat']

            place_json['lng'] = lng
            place_json['lat'] = lat

            filtered_places.append(place_json)
            # break

        pprint(filtered_places)
        return HttpResponse(filtered_places, content_type='application/json')


class SearchObject(APIView):
    """
    EXPECT:
        GET Request coming with one JSON entries in data:
            place_id: <Str>
    EXAMPLE: 
        curl -X GET http://localhost:8000/trip/search/loc/ -d "place_id"="ChIJpbxvgcW8woARAfXIdZBKSsY"
    RETURN:
        JSON containing all details of the place
    """
    def __get_place_detail(self, place_id:str):
        resp = gmaps.place(place_id)
        pprint(resp)
        return resp

    def get(self, request, format=None):
        # retrieving data
        data = request.data
        if not 'place_id' in data:
            raise ParseError(detail="Expecting a string field 'place_id'.", code=None)

        place_id = data['place_id']
        resp = self.__get_place_detail(place_id)

        return HttpResponse(resp, content_type='application/json')
