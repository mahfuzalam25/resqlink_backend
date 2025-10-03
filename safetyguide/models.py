from django.db import models
from django.core.exceptions import ValidationError
import os

# Create your models here.
def image_validator(value):
    ext = os.path.splitext(value.name)[1]
    validExtension = ['.jpg','.jpeg', '.png','.svg','.webp']
    if not ext.lower() in validExtension:
        raise ValidationError(f'Unsupported file extension: {ext}. Allowed extensions are: .jpg, .jpeg, .png, .webp, .svg')


class SafetyGuide(models.Model):
    icon = models.FileField(upload_to='profile/', validators=[image_validator], null=True, blank=True)
    title = models.CharField(max_length=124, blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.id}'

class SafetyAdvice(models.Model):
    guide = models.ForeignKey(SafetyGuide, related_name='advices', on_delete=models.CASCADE)
    text = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f'{self.text} - {self.id}'

