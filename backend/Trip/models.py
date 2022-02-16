from django.db import models
# from User.models import UserProfile
from django.contrib.auth.models import User


"""
data model for a itinerary (consists of 0 or more non-overlapping TripEvent)
"""
class Itinerary(models.Model):
    # itin_id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=64, null=True)
    desc = models.TextField(max_length=500, blank=True, default="Edit this to be the description of your travel plan!")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="itinerary") # related_name solves the problem of 'User' object has no attribute 'itinerary'

    # timestamp for created and last updated
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        return title[itin_id] of the trip itinerary
        """
        return str(self.title) + "[" + str(self.user) + "]"

"""
data model for a specific trip event (an attraction/restaurant/hotel...) that has start time and end time
"""
class TripEvent(models.Model):
    # object ID of OpenTripMap API (single attraction)
    xid = models.CharField(max_length=64)
    # foreign key indicating which itinerary it belongs to
    itin = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name="trip_event")
    start_time = models.TimeField()
    end_time = models.TimeField()


    def __str__(self):
        """
        return xid (object_ID) of the trip event
        """
        return str(self.xid)

