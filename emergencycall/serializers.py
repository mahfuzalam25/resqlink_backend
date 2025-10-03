from rest_framework import serializers
from .models import StationCatagory, StationInfo


class EmergencyCallListSerializers(serializers.ModelSerializer):
    class Meta:
        model = StationInfo
        fields = ['id', 'station_name', 'phone','station_location']

class EmergencyCallSerializers(serializers.ModelSerializer):
    info = EmergencyCallListSerializers(many=True, read_only=True)

    class Meta:
        model = StationCatagory
        fields = ['id','station_title','info']