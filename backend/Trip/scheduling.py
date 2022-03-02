"""
Generate schedules for a list of input places
"""
from .googlemap_api import SearchLocation, ATTRACTION_TYPES, RADIUS
import requests
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsAdmin, IsOwnerOrAdmin
from .models import Itinerary, TripEvent
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
import json
import random
from pprint import pprint
import pytz
from datetime import datetime, timedelta
from tzwhere import tzwhere
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib
matplotlib.use('Agg')
# k_means_constrained does not support arm64 (m1 mac)
CONSTRAINED_KMEANS = False
try:
    from k_means_constrained import KMeansConstrained as KMeans
    CONSTRAINED_KMEANS = True
except ImportError:
    from sklearn.cluster import KMeans
# from clustering.equal_groups import EqualGroupsKMeans as KMeans
# from k_means_constrained import KMeansConstrained as KMeans


# CONFIG
MIN_PLACES_PER_DAY = 3
MAX_PLACES_PER_DAY = 4
TOURIST = "tourist_attraction"
# this number specifies how many times Google Place API will be queried when extending places to visit (due to user does not supply enough places for scheduling)
SEARCH_LIMIT = 3
START_DATETIME = datetime(2022, 2, 22, 8, 30)
TIME_FOR_WAKEUP = timedelta(hours=1)
# TODO: currently we fixed 30 minutes as the interval for two places to visit, should've consider real-time traffic for this
TIME_FOR_TRAFFIC = timedelta(minutes=30)

# FOR TESTING


class Place:
    """
    A place object, used as the base unit in scheduling
    """

    def __init__(self, place_json: dict):
        self.name = place_json['name']
        self.lng = float(place_json['geometry']['location']['lng'])
        self.lat = float(place_json['geometry']['location']['lat'])
        self.rating = 3.5  # default rating
        if 'rating' in place_json:
            self.rating = float(place_json['rating'])
        self.place_id = place_json['place_id']
        # original json data for sending back to frontend
        self.json = place_json
        self.start_time = None
        # NOTE: right now we hardcode 2.5 hrs for each place to visit
        self.duration = timedelta(hours=2, minutes=30)

    def to_list(self):
        # to work with sklearn K-Means
        return [self.lng, self.lat]

    @staticmethod
    def l2_distance(p1, p2):
        return np.sqrt((p1.lng - p2.lng)**2 + (p1.lat - p2.lat)**2)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Place(" + self.name + ")"

    def __eq__(self, other):
        return other.place_id == self.place_id

    def __hash__(self):
        return hash(self.place_id)


class Scheduler:
    """
    A scheduler class that handles travel plan scheduling
    """

    def __init__(self, place_list: list[Place], days: int, hotel: Place = None):
        self.place_list = place_list
        self.days = days
        self.hotel = hotel

        # determine timezone based on average coordinates
        avg_lat, avg_lng = 0, 0
        for p in place_list:
            avg_lat += p.lat
            avg_lng += p.lng
        avg_lat, avg_lng = avg_lat/len(place_list), avg_lng/len(place_list)
        tw = tzwhere.tzwhere()
        timezone_str = tw.tzNameAt(avg_lat, avg_lng)
        tzinfo = pytz.timezone(timezone_str)

        self.timezone = tzinfo
        self.timezone_str = timezone_str

        # scheduling result: list of sub place_list for each day (ORDERED)
        self.itineraries = []

    def __str__(self):
        scheduler_str = ""
        cnt = 0
        for place in self.place_list:
            scheduler_str += "[" + str(cnt) + "]: " + str(place) + "\n"
            cnt += 1

        return scheduler_str

    @staticmethod
    def visualizer(place_list: list[list[Place]], save_name="./schedule_plot.png"):
        color = cm.rainbow(np.linspace(0, 1, len(place_list)))
        for l, c in zip(place_list, color):
            # choose a color
            px = [p.lng for p in l]
            py = [p.lat for p in l]
            plt.scatter(px, py, c=c)

        plt.savefig(save_name)

    @staticmethod
    def __find_nearest(p: Place, p_list: list[Place]):
        nearest_distance = float('inf')
        nearest_place = None
        for candidate in p_list:
            candidate_distance = Place.l2_distance(p, candidate)
            if candidate_distance < nearest_distance:
                nearest_distance = candidate_distance
                nearest_place = candidate

        return nearest_place

    @staticmethod
    def __kmeans(place_list, days, max_places_per_day=4):
        # run k means on place_list
        # num_clusters = days
        # num_of_datapoints = len(place_list)
        places_array = np.array([p.to_list() for p in place_list])
        # NOTE: sklearn's KMeans does not have max_size constraints on each cluster
        #           it only works with k_means_constrained package
        kwargs = {}
        if CONSTRAINED_KMEANS:
            kwargs['size_max'] = max_places_per_day
        model = KMeans(n_clusters=days, n_init=30, **kwargs)
        cluster = model.fit_predict(places_array)

        # #_of_days empty list
        cluster_result = [[] for _ in range(days)]
        # split the places into lists of list
        for i in range(len(place_list)):
            which_cluster = cluster[i]
            cluster_result[which_cluster].append(place_list[i])

        return cluster_result

    def schedule(self, wakeup_datetime):
        """
        turn self.place_list: list[Place] into list[list[Place]], each outer list represent 1 day
        """
        # tranform string typed wakeup_datetime into datetime format
        wakeup_datetime = datetime.strptime(wakeup_datetime, "%Y-%m-%d %H:%M")

        print(
            f"[Scheduling for {len(self.place_list)} places in {self.days} days...]")
        current_schedule_time = wakeup_datetime + TIME_FOR_WAKEUP
        day_offset = timedelta(days=0)
        # run kmeans algorithm
        cluster_result = self.__kmeans(
            self.place_list, self.days, MAX_PLACES_PER_DAY)
        # after we got clustering for each day, we can start re-ordering the places within each day
        scheduled_result = []
        for each_day_places in cluster_result:
            # set the starting time for each day
            current_schedule_time = wakeup_datetime + TIME_FOR_WAKEUP + day_offset
            # init schedule result
            each_day_scheduled_result = []
            starting_place = None
            # choosing a starting place
            if not self.hotel:
                starting_place = random.choice(each_day_places)
            else:
                # sort places by the l2 distance to the hotel
                starting_place = each_day_places.sort(
                    key=lambda p: Place.l2_distance(p, self.hotel))[0]
            # assign time to starting place
            starting_place.start_time = current_schedule_time
            current_schedule_time += starting_place.duration
            current_schedule_time += TIME_FOR_TRAFFIC
            # add starting place to schedule list
            each_day_places.remove(starting_place)
            each_day_scheduled_result.append(starting_place)

            print(
                f"+++-> {starting_place.name[:6]}... has scheduled at {starting_place.start_time}")

            # got the starting place for each day, find the nearest neighbor and add it to place
            current_place = starting_place
            while len(each_day_places) > 0:
                next_place = self.__find_nearest(
                    current_place, each_day_places)
                # assign time to currently scheduling place
                next_place.start_time = current_schedule_time
                current_schedule_time += next_place.duration
                current_schedule_time += TIME_FOR_TRAFFIC
                # add current scheduling place to schedule list
                each_day_places.remove(next_place)
                each_day_scheduled_result.append(next_place)
                print(
                    f"+++ {next_place.name[:6]}... has scheduled at {next_place.start_time}")
                current_place = next_place

            scheduled_result.append(each_day_scheduled_result)

            # advance another day
            day_offset += timedelta(days=1)

        return scheduled_result


class SchedulingTEST(SearchLocation):
    """
    Overwriting GET method for tesing, the test api endpoint is:
        GET http://127.0.0.1:8000/trip/schedule/test?location=Los%20Angeles
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
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ2MjA5OTA1LCJpYXQiOjE2NDYxMjM1MDUsImp0aSI6IjkxMjAxZjkzMzZiMDRhYjJhMzQ2MGM0ZDVhMmZhNTIxIiwidXNlcl9pZCI6MX0.JufpAe_Er3zdQWgqMciiLUfidt9MKKi4zSUQ7zFWZMM'
        }
        simulated_data = {
            "places": nearby_places,
            "dates": [
                "2022-03-03",
                "2022-03-04",
                "2022-03-05",
                "2022-03-06",
                "2022-03-07",
                "2022-03-08"
            ],
            "wakeUpTime": "09:00"
        }
        simulated_data = json.dumps(simulated_data)
        response = requests.post(
            "http://127.0.0.1:8000/trip/schedule/", data=simulated_data, headers=headers)
        return HttpResponse(response)


class SchedulingAPI(APIView):
    """
    Accepting POST request with data body like this:
    {
        "userOptions":{
            "places": [
                {},
                {},
                ...
            ],
            "wakeUpTime": “<WAKE-UP-TIME-FORMAT>”,
            "dates": ["<DATE-1>", "<DATE-2>", "<DATE-3>"],
            "hotel": {} # this field optional
        }
    }

    Returning 200 OK with newly generated id in data body:
    {
        "id": <ID-OF-GENERATED-ITINERARY>
    }
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def __radius_based_on_days(self, days):
        """
        generate a searching radius (in meter) based on days spent on the trip:
            - the longer the trip, the larger the radius.
        """
        radius = 0
        if days < 3:
            radius = 10  # km
        elif days < 7:
            radius = 50  # km
        elif days < 14:
            radius = 100  # km
        else:
            radius = 300  # km

        return radius * 1000

    def __auto_extension_strategy(self, places: list[dict], days: int, minimum_places_per_day: int, maximum_places_per_day: int, search_limit: int):
        """
        An extension Strategy takes as input places, and extend them to required number of places for scheduling (minimum_places_per_day * days)
        @params places      : list of dict, received from front-end requesting scheduling for these places
        @params days        : int, how many days to stay for this travel plan
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

        print(
            f"[Received {len(place_list)} places, scheduling for {days} days...]")

        # sanity check
        # check number of places
        num_places = len(place_list)
        if num_places == 0:
            raise ParseError(detail="Expect at least 1 place selected.")
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
                searched_places = SearchLocation._SearchLocation__find_places_in_radius(
                    coord, search_radius, type=TOURIST)
                searched_place_list = []
                for searched_place in searched_places:
                    sp = Place(searched_place)
                    # skip repeated places
                    if sp in place_set:
                        continue
                    searched_place_list.append(sp)
                # print(f"[Searched {len(searched_place_list)} places]")
                # only keep the good part per query (if searched enough places)
                if len(searched_place_list) > NUM_TO_KEEP_PER_SEARCH:
                    searched_place_list = searched_place_list[:NUM_TO_KEEP_PER_SEARCH]
                # print(f"[Keeped {len(searched_place_list)} places]")
                # put them into place_list for scheduling
                place_list.extend(searched_place_list)
                for sp in searched_place_list:
                    place_set.add(sp)
                # enlarge search radius each time if does not got enough places
                search_radius *= 2

        return place_list[:MAX_PLACES_PER_DAY * days]

    def post(self, request, format=None):
        data = request.data
        places = data['places']
        dates = data['dates']
        wakeup_time = data['wakeUpTime']
        wakeup_datetime = dates[0] + " " + wakeup_time
        days = len(dates)
        hotel = None
        if 'hotel' in data:
            hotel = data['hotel']

        # sanity check
        if not isinstance(places, list):
            raise ParseError(
                detail=f"Places should be list of jsons.", code=None)
        if not isinstance(dates, list):
            raise ParseError(
                detail=f"Dates should be list of strings.", code=None)

        """
        this extension strategy will search SEARCH_LIMIT times given MIN_PLACES_PER_DAY,
            it will extend current number of places to MIN_PLACES_PER_DAY * days if it's less than this threshold.
            also it will truncated places if exceeds MAX_PLACES_PER_DAY * days.
        """
        place_list = self.__auto_extension_strategy(
            places, days, MIN_PLACES_PER_DAY, MAX_PLACES_PER_DAY, SEARCH_LIMIT)

        # for p in place_list: print(p)
        # init a scheduler
        S = Scheduler(place_list=place_list, days=days, hotel=hotel)
        # scheduling -> list[list[Place]], expecting time format: "%Y-%m-%d %H:%M"
        scheduled_lists = S.schedule(wakeup_datetime=wakeup_datetime)

        # Visualizing! (Be sure to comment this off in production)
        Scheduler.visualizer([place_list, ], save_name="./input_plot.png")
        Scheduler.visualizer(scheduled_lists)

        print("[Debug]: Turning Scheduled Results into Itinerary...")
        # create an empty Itinerary for user
        new_itinerary = Itinerary(
            title="Your Auto Scheduled Trip",
            user=request.user
        )
        new_itinerary.save()

        # create each place as an TripEvent, and associate with the Itinerary
        for each_day_places in scheduled_lists:
            for p in each_day_places:
                print("=>=>=>=> START TIME =>=>=>: ",
                      datetime.strftime(p.start_time, "%Y-%m-%d %H:%M"))
                print("=>=>=>=> END TIME =>=>=>: ", datetime.strftime(
                    p.start_time + p.duration, "%Y-%m-%d %H:%M"))
                new_tripevent = TripEvent(
                    place_id=p.place_id,
                    place_name=p.name,
                    itin=new_itinerary,
                    start_time=p.start_time,
                    end_time=(p.start_time + p.duration),
                    lat=p.lat,
                    lng=p.lng
                )
                new_tripevent.save()

        # return the newly generated itinerary back to front-end
        resp = {
            "id": new_itinerary.id
        }
        return HttpResponse(json.dumps(resp), content_type='application/json')
