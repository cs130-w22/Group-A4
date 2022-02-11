from django.contrib import admin
from .models import Itinerary, TripEvent

# Register your models here.
admin.site.register(Itinerary)
admin.site.register(TripEvent)