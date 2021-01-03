from django.urls import path
from location import api
from rest_framework import routers


urlpatterns = [
    path('api/location/test', api.ConnectionTest.as_view()),
    path('api/location/upload', api.GetLatLongAPI.as_view()),
]