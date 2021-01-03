from django.urls import path
from location import api
from rest_framework import routers


urlpatterns = [
    path('api/location/upload', api.GetLatLongAPI.as_view()),
]