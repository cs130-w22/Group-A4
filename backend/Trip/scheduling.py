"""
Generate schedules for a list of input places
"""
import json
import random
from pprint import pprint
from datetime import datetime
from numpy import place

from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from django.http import HttpResponse

# CONFIG
MINIMUM_PLACES_PER_DAY = 3
TOURIST = "tourist_attraction"
SEARCH_LIMIT = 3 # this number specifies how many times Google Place API will be queried when extending places to visit (due to user does not supply enough places for scheduling)

# FOR TESTING
import requests
from .googlemap_api import SearchLocation, ATTRACTION_TYPES, RADIUS


class Place:
    """
    A place object, used as the base unit in scheduling
    """
    def __init__(self, place_json:dict):
        self.name = place_json['name']
        self.lng = float(place_json['geometry']['location']['lng'])
        self.lat = float(place_json['geometry']['location']['lat'])
        self.rating = float(place_json['rating'])
        self.place_id = place_json['place_id']
        # original json data for sending back to frontend
        self.json = place_json

    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return other.place_id == self.place_id

    def __hash__(self):
        return hash(self.place_id)

class Scheduler:
    """
    A scheduler class that handles travel plan scheduling
    """
    def __init__(self, place_list:list[Place], days:int, hotel:Place=None):
        self.place_list = place_list
        self.days = days
        self.hotel = hotel

        # scheduling result: list of sub place_list for each day (ORDERED)
        self.itineraries = []
    
    def __str__(self):
        scheduler_str = ""
        cnt = 0
        for place in self.place_list:
            scheduler_str += "[" + str(cnt) + "]: " + str(place) + "\n"
            cnt += 1
        
        return scheduler_str

        
    def schedule(self):
        print(f"Scheduling for {len(self.place_list)} places in {self.days} days...")


class SchedulingTEST(SearchLocation):
    """
    Overwriting GET method for tesing
    """
    def get(self, request):
        # sanity checks
        if not 'location' in request.GET:
            raise ParseError(
                detail="Expecting a string field 'location' indicating the destination for recommendation.", code=None)

        location = request.GET['location']
        # get coordinates based on name of the places (lat, lng)
        coord = self._SearchLocation__get_coord_by_name(location)

        # NOTE: because google map api only support 1 type restriction per query,
        #       so need to send 1 request per place's type.
        nearby_places = []
        for TYPE in ATTRACTION_TYPES:
            print(f"Searching for TYPE = {TYPE}...")
            # use the coordinates to retrieve nearby places of interests
            nearby_places.extend(self._SearchLocation__find_places_in_radius(
                coord, radius=RADIUS, type=TYPE))
        
        print("SIMULATING START....")
        # SIMULATING FRONTEND, POST TO http://127.0.0.1/trip/schedule/
        headers = {'Content-Type': 'application/json'}
        simulated_data = {
            "places": nearby_places,
            "days": 3
        }
        simulated_data = json.dumps(simulated_data)
        response = requests.post("http://127.0.0.1:8000/trip/schedule/", data=simulated_data, headers=headers)
        return HttpResponse(response)


class SchedulingAPI(APIView):
    """
    Accepting POST request with data body like this:
    {
        "places": [
            {},
            {},
            ...
        ],
        "days": 3,
        "hotel": {}
    }
    """
    def __radius_based_on_days(self, days):
        """
        generate a searching radius (in meter) based on days spent on the trip:
            - the longer the trip, the larger the radius.
        """
        radius = 0
        if days < 3:
            radius = 10 # km
        elif days < 7:
            radius = 50 # km
        elif days < 14:
            radius = 100 # km
        else:
            radius = 300 # km
        
        return radius * 1000

    def __zb_extension_strategy(self, places:list[dict], days:int, minimum_places_per_day:int, search_limit:int):
        """
        An extension Strategy takes as input places, and extend them to required number of places for scheduling (minimum_places_per_day * days)
        @params places      : list of dict, received from front-end requesting scheduling for these places
        @params days        : int, how many days to stay in this travel plan
        @params minimum_places_per_day
                            : a minimum requirement of how many places a user will visit
        @params search_limit: at most how many times this function will query Google Place API
        @RETURN place_list  : list of Place object, used for scheduling
        """
        # create Place object before put them to extension
        place_list = []
        place_set = set()
        for place_json in places:
            p = Place(place_json)
            place_list.append(p)
            place_set.add(p)

        print(f"Received {len(place_list)} places, scheduling for {days} days...")

        # sanity check
        # check number of places
        num_places = len(place_list)
        if num_places == 0:
            raise ParseError(detail="Expect number of places selected greater than 0.")
        elif num_places < minimum_places_per_day * days:
            # extend places to at least minimum_places_per_day * days
            # calculate average (rounded) number of places to keep per Google search query
            NUM_TO_BE_SEARCHED = minimum_places_per_day * days - num_places
            NUM_TO_KEEP_PER_SEARCH = NUM_TO_BE_SEARCHED // search_limit + 1
            starting_radius = self.__radius_based_on_days(days)
            # search based on this randomly picked place from User input
            randomly_picked_place = random.choice(place_list)
            coord = (randomly_picked_place.lat, randomly_picked_place.lng)
            # break the loop only if searched enough places for scheduling
            search_radius = starting_radius
            while len(place_list) < minimum_places_per_day * days:
                searched_places = SearchLocation._SearchLocation__find_places_in_radius(coord, search_radius, type=TOURIST)
                searched_place_list = []
                for searched_place in searched_places:
                    sp = Place(searched_place)
                    if sp in place_set:
                        continue
                    searched_place_list.append(sp)
                print(f"Searched {len(searched_place_list)} places")
                # only keep the good part per query (if searched enough places)
                if len(searched_place_list) > NUM_TO_KEEP_PER_SEARCH:
                    searched_place_list = searched_place_list[:NUM_TO_KEEP_PER_SEARCH]
                print(f"Keeped {len(searched_place_list)} places")
                # put them into place_list for scheduling
                place_list.extend(searched_place_list)
                for sp in searched_place_list: place_set.add(sp)
                # enlarge search radius each time if does not got enough places 
                search_radius *= 2
        
        return place_list

    def post(self, request, format=None):
        data = request.data
        places = data['places']
        days = data['days']
        hotel = None
        if 'hotel' in data:
            hotel = data['hotel']

        # NOTE: ONLY FOR TESTING, DELETE IMMEDIATELY
        places = places[:2]
        # NOTE: ONLY FOR TESTING, DELETE IMMEDIATELY

        """
        this extension strategy will search SEARCH_LIMIT times given MINIMUM_PLACES_PER_DAY,
            it will extend current number of places to MINIMUM_PLACES_PER_DAY * days if it's less than this threshold.
        """
        place_list = self.__zb_extension_strategy(places, days, MINIMUM_PLACES_PER_DAY, SEARCH_LIMIT)
        
        # only pick the top MINIMUM_PLACES_PER_DAY * days places
        place_list = place_list[:MINIMUM_PLACES_PER_DAY * days]
        print("Total number of places for scheduling: ", len(place_list))
        for p in place_list: print(p)
        # init a scheduler
        S = Scheduler(place_list=place_list, days=days, hotel=hotel)
        
        return HttpResponse(request.data, content_type='application/json')

        

