from django.shortcuts import render
from rest_framework import generics,filters
from .models import StationCatagory, StationInfo
from .serializers import EmergencyCallSerializers,EmergencyCallListSerializers
# Create your views here.

class EmergencyCallListView(generics.ListAPIView):
    queryset = StationCatagory.objects.all()
    serializer_class = EmergencyCallSerializers


class StationInfoSearchView(generics.ListAPIView):
    queryset = StationInfo.objects.all()
    serializer_class = EmergencyCallListSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['station_location']