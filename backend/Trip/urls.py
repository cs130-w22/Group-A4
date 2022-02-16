from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # search API Endpoints
    path('search/id/', views.search_object, name="trip_search"),
    path('search/loc/', views.SearchLocation.as_view(), name="trip_search"),
    # TripEvent API Endpoints
    path('event/create/', views.TripEventCreate.as_view(), name="tripevent_create"),
    # path('event/', views.TripEventList.as_view(), name="tripevent_detail"),
    path('event/<int:pk>/', views.TripEventUpdate.as_view(), name="tripevent_update"),
    # Itinerary API Endpoints
    path('itinerary/create/', views.ItineraryCreate.as_view(), name="itinerary_create"),
    path('itinerary/', views.ItineraryList.as_view(), name="itinerary_list"),
    path('itinerary/<int:pk>/', views.ItineraryViewUpdate.as_view(), name="itinerary_view_update"),
    path('itinerary/all/', views.ItineraryListAll.as_view(), name="itinerary_list_all"),
]
