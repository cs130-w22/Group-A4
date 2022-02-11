from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # search API Endpoints
    path('search/id', views.search_object, name="trip_search"),
    path('search/loc', views.search_loc, name="trip_search"),
    # CRUD API Endpoints
    path('event/', views.TripEventCRUD.as_view(), name="tripevent_detail"),
    path('itinerary/create/', views.ItineraryCreate.as_view(), name="itinerary_create"),
    path('itinerary/', views.ItineraryList.as_view(), name="itinerary_list"),
]
