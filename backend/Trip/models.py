from django.db import models
# from User.models import UserProfile


"""
class model for a specific trip event (travel plan) that belong to specific user.
"""
class TripEvent(models.Model):
    title = models.CharField(max_length=64, null=True)
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    desc = models.TextField(max_length=500, blank=True, default="Edit this to be the description of your travel plan!")
    start_time = models.TimeField()
    end_time = models.TimeField()

    # timestamp for created and last updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        """
        return title of the trip event
        """
        return str(self.title)

