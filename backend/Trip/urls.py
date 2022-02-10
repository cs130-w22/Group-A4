from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('search/id', views.search_object, name="trip_search"),
    path('search/loc', views.search_loc, name="trip_search"),
]
