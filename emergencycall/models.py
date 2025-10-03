from django.db import models
from django.core.exceptions import ValidationError
import os
# Create your models here.

def image_validator(value):
    ext = os.path.splitext(value.name)[1]
    validExtension = ['.jpg','.jpeg', '.png','.svg','.webp']
    if not ext.lower() in validExtension:
        raise ValidationError(f'Unsupported file extension: {ext}. Allowed extensions are: .jpg, .jpeg, .png, .webp, .svg')

class StationCatagory(models.Model):
    station_title = models.CharField(max_length=124, blank=True, null=True)
    # icon = models.FileField(upload_to='profile/', validators=[image_validator], null=True, blank=True)

    def __str__(self):
        return f'{self.station_title}-{self.id}'

class StationInfo(models.Model):
    station_Catagory = models.ForeignKey(StationCatagory, related_name='info', on_delete=models.CASCADE)
    station_name = models.CharField(max_length=60, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    station_location = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f'{self.station_name} - {self.station_location}'



